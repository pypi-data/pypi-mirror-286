import logging 
import time
import requests
from bs4 import BeautifulSoup
import bs4
import json
import yaml
from typing import List, Dict, Any, Union, Callable
from functools import wraps
logger = logging.getLogger(__name__)


class hypertext:
    '''
    hypertext class -- 
    A class for extracting and manipulating HTML content into structured data.
    '''
    class ELEMENTS:
        TEXT = ['p', 'span', 'a']
        BLOCK = ['div', 'section', 'article', 'nav', 'aside', 'header', 'footer', 'main']
        INLINE = ['b', 'i', 'u', 'strong', 'em', 'abbr', 'cite', 'code', 'q', 'sub', 'sup', 'time']
        HEADING = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        MEDIA = ['img', 'audio', 'video', 'source']
        LIST = ['ul', 'ol', 'li', 'dl', 'dt', 'dd']
        TABLE = ['table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td']
        FORM = ['form', 'input', 'textarea', 'button', 'select', 'option', 'label', 'fieldset', 'legend']
        SCRIPT = ['script', 'noscript']
        META = ['meta', 'link', 'style', 'title', 'base']
        URLS = ['href', 'src', 'data-src', 'action']

    @staticmethod
    def fetch(url, cookies=None, headers=None, params=None):
        '''
        request the content of a URL
        '''
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return None

    @staticmethod
    def filters(filterfor=None, filterout=None):
        '''
        filter the schema based on the selector(s)
        '''
        def decorator(func):
            @wraps(func)
            def wrapper(schema):
                if not schema:
                    return None
                if filterfor and schema['selector'] not in filterfor:
                    # Check if any children match the filter
                    fChildren = [
                        wrapper(child) for child in schema['children']
                    ]
                    fChildren = [child for child in fChildren if child]
                    if fChildren:
                        return {**schema, 'children': fChildren}
                    return None
                if filterout and schema['selector'] in filterout:
                    return None
                # Recursively filter children
                schema['children'] = [
                    wrapper(child) for child in schema['children']
                ]
                schema['children'] = [child for child in schema['children'] if child]
                return schema
            return wrapper
        return decorator
    
    def __init__(self, content):
        self.content = content
        self.soup = BeautifulSoup(content, 'html.parser')

    def Extract(self, element, target):
        '''
        extract specific data from an element
        '''
        def Links(element):
            urls = {}
            for attr in self.ELEMENTS.URLS:
                if element.has_attr(attr):
                    urls[attr] = element[attr]
            return urls
        if target == 'links':
            return Links(element)


    def Schematize(self, method='dict', filterfor=None, filterout=None):
        '''
        convert the HTML content into a structured schema
        '''
        def Schema(element):
            def FullPath(element):
                path = []
                for parent in element.parents:
                    if parent.name == '[document]':
                        break
                    selector = parent.name
                    if parent.get('id'):
                        selector += f'#{parent.get("id")}'
                    elif parent.get('class'):
                        selector += f'.{parent.get("class")[0]}'
                    path.append(selector)
                return ' > '.join(reversed(path))
            if not isinstance(element, bs4.element.Tag):
                return None
            schematic = {
                'selector': element.name,
                'class': element.get('class', []),
                'id': element.get('id', ''),
                'path': FullPath(element),
                'content': element.get_text(strip=True),
                'count': 1,
                'children': []
            }
            urls = self.Extract(element, 'links')
            if urls:schematic['urls'] = urls
            for child in element.children:
                cSchema = Schema(child)
                if cSchema:
                    schematic['children'].append(cSchema)
            return schematic
        fullschema = Schema(self.soup)
        if filterfor or filterout:
            @self.filters(filterfor, filterout)
            def clean(schema):
                return schema
            schema = clean(fullschema)
        else:
            schema = fullschema
        if not schema:
            logger.warning("No elements passed the filter or no valid HTML structure found.")
            return {}
        if method == 'json':
            return json.dumps(schema, indent=2)
        elif method == 'yaml':
            return yaml.dump(schema)
        return schema

class schematix:
    '''
    helper class for interacting with extracted schemas
    '''
    @staticmethod
    def extraction(condition: Callable, schema: Dict, target: List[str], level: Union[int, List, range] = None) -> List[Any]:
        results = []
        
        logger.debug(f"Debug: Starting extraction with target {target} and level {level}")
        logger.debug(f"Debug: Schema keys: {list(schema.keys())}")
        
        def recursive(node: Any, current: int = 0):
            logger.debug(f"Debug: Processing node at level {current}, type: {type(node)}")
            
            if isinstance(node, str):
                if condition(node):
                    results.append(node)
                return
            
            if isinstance(node, list):
                for item in node:
                    recursive(item, current)
                return
            
            if not isinstance(node, dict):
                logger.debug(f"Debug: Unexpected node type: {type(node)}")
                return
            
            if level is not None:
                if isinstance(level, int) and current > level:
                    return
                if isinstance(level, List) and current not in level:
                    return
                if isinstance(level, range) and current not in level:
                    return
            
            selector = node.get('selector')
            if selector in target:
                logger.info(f"Debug: Found target selector: {selector}")
                if 'urls' in node:
                    for typeof, url in node['urls'].items():
                        if condition(url):
                            results.append(url)
                if 'content' in node and condition(node['content']):
                    results.append(node['content'])
            
            for child in node.get('children', []):
                recursive(child, current + 1)
        
        for rootkey, rootelement in schema.items():
            logger.debug(f"Debug: Processing root element: {rootkey}")
            recursive(rootelement)
        
        logger.info(f"Extraction complete. Found {len(results)} results.")
        return results

    @staticmethod
    def findelements(schema: Dict, selector: str, attributes: Dict = None, content: str = None) -> List[Dict]:
        results = []
        
        logger.debug(f"Debug: Starting findelements with selector {selector}, attributes {attributes}, content filter: {'Yes' if content else 'No'}")

        def searchrecursive(node: Dict):
            logger.debug(f"Debug: Searching node: {node.get('selector', 'Unknown')}")
            if node['selector'] == selector:
                logger.debug(f"Debug: Found matching selector: {selector}")
                if attributes:
                    if all(value in node.get(attr, []) for attr, value in attributes.items()):
                        logger.debug(f"Debug: Attributes match for node: {node.get('selector')}")
                        if content is None or content in node.get('content', ''):
                            logger.debug(f"Debug: Content match (or no content filter). Adding to results.")
                            results.append(node)
                    else:
                        logger.debug(f"Debug: Attributes do not match for node: {node.get('selector')}")
                elif content is None or content in node.get('content', ''):
                    logger.debug(f"Debug: No attribute filter. Content match (or no content filter). Adding to results.")
                    results.append(node)

            for child in node.get('children', []):
                searchrecursive(child)

        for rootkey, rootelement in schema.items():
            logger.debug(f"Debug: Searching root element: {rootkey}")
            searchrecursive(rootelement)

        logger.info(f"findelements complete. Found {len(results)} results.")
        return results