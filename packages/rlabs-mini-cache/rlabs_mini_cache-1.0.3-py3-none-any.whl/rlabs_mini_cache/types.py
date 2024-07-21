'''
    Types
'''
from datetime import datetime
from typing import TypedDict
from typing import TypeAlias


ParsedJsonData: TypeAlias = dict | list

class CacheEntry(TypedDict):
    '''
        Cache Entry
    '''
    data: ParsedJsonData
    timestamp: datetime

LoadedCache: TypeAlias = dict[str, CacheEntry]
