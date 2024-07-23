import logging 
import time
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
import requests
import json
import yaml
from typing import List, Dict, Any, Union, Callable, Tuple
from collections import defaultdict
from itertools import combinations
logger = logging.getLogger(__name__)


class PayloadFuzzer:
    '''
    Context Manager for producing all possible variations for a given payload
    '''
    def __init__(self, payload:Dict[str, Any], fuzzable:List[Any], funcs: Dict[str, Callable]):
        self.original = payload
        self.fuzzed = [self.original]
        self.fuzzable = fuzzable
        self.funcs = funcs or {}
    def __enter__(self):
        self.fuzz() 
        return self.fuzzed
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def fuzz(self):
      #custom functions
        for key, func in self.funcs:
            if key in self.fuzzable:
                self.fuzzed.extend(func(self.original))
        for r in range(1, len(self.fuzzable) + 1):
            for combo in combinations(self.fuzzable, r):
                new = self.original.copy()
                for field in combo:
                    new[field] = None
                if new not in self.fuzzed:
                    self.fuzzed.append(new)

        for i, f1 in enumerate(self.fuzzable):
            for f2 in self.fuzzable[i+1]:
                if type(self.original[f1]) == type(self.original[f2]):
                    new = self.original.copy()
                    new[f1], new[f2] = new[f2], new[f1]
                    if new not in self.fuzzed:
                        self.fuzzed.append(new)
    
    def register(self, key:str, func:Callable):
        '''
        Register a custom function to fuzz a specific field
        '''
        self.funcs[key] = func
           

    
def farthestextent(func, payload, paginator:str = 'page', reach:Tuple[int, int]=(1, 100)) -> int:
    '''
    Find the farthest extent of a paginated request
    '''
    left, right = reach
    lastresponse = None
    allresponses = []
    while left <= right:
        mid = (left + right) // 2
        payload[paginator] = mid
        response = func(payload)
        if response:
            lastresponse = response
            allresponses.extend(response)
            left = mid + 1
        else:
            right = mid - 1
    return max(allresponses)


def recursively(func, pkwarg:Union[str, int] = 'payload', paginator: str = 'page', breakat:Union[int, Callable] = 50, retries: int = 3):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = kwargs.get(pkwarg) if kwargs.get(pkwarg) and type(pkwarg)==str else args[pkwarg] if type(pkwarg)==int else args[0]
        start = int(payload.get(paginator, 1))
        if type(breakat)== Callable:breakat = breakat(func, payload)
        allpayloads = []
        for i in range(start, breakat + 1):
            new = payload.copy()
            new[paginator] = i
            allpayloads.append(new)
        results = []
        failed = defaultdict(int)
        def tracking(payload):
            nonlocal results, failed
            page = payload[paginator]
            data = func(payload)
            if data:results.extend(data)
            else:failed[page] += 1
            return data
        with ThreadPoolExecutor() as executor:
            list(executor.map(tracking, allpayloads))
        for _ in range(retries):
            if not failed:
                break
            toretry = []
            for page, failcount in list(failed.items()):
                if failcount <= retries:
                    new = payload.copy()
                    new[paginator] = page
                    toretry.append(new)
                    del failed[page]
            with ThreadPoolExecutor() as executor:
                list(executor.map(tracking, toretry))
        for page, failcount in failed.items():
            logger.warning(f"Page {page} failed after {failcount} attempts")
        return results
    return wrapper