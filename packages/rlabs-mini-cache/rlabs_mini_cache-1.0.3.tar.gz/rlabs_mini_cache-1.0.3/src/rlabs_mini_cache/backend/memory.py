'''
    Memory
'''
from datetime import datetime
from typing import Callable
from datetime import timedelta
from typing import Optional

from rlabs_mini_cache.backend.base import Backend
from rlabs_mini_cache.error import CacheMissNotFound
from rlabs_mini_cache.error import CacheMissGracefulDegradation
from rlabs_mini_cache.types import LoadedCache
from rlabs_mini_cache.types import ParsedJsonData
from rlabs_mini_cache.backend.base import LoadedFrom

class Memory(Backend):
    '''
        Memory Backend
    '''
    def __init__(
            self,
            max_age: timedelta,
            read_fn: Optional[Callable[..., ParsedJsonData]] = None,
        ) -> None:
        '''
            Init
        '''
        super().__init__(
            max_age,
            self.__class__,
            read_fn
        )

        self.cache_data: LoadedCache = {}

    def _cache_init(
            self
        ) -> None:
        '''
            Cache init
        '''
        pass

    def _cache_invalidate(
            self
        ) -> None:
        '''
            Cache invalidate
        '''
        self.cache_data = {}

    def _cache_read_data(
            self,
            key: str
        ) -> ParsedJsonData:
        '''
            Cache read data
        '''
        if key not in self.cache_data:
            raise CacheMissNotFound()

        return self.cache_data[key]['data']

    def _cache_read_timestamp(
            self,
            key: str
        ) -> tuple[datetime, LoadedFrom]:
        '''
            Cache read timestamp
        '''
        if key not in self.cache_data:
            raise CacheMissNotFound()

        return self.cache_data[key]['timestamp'], LoadedFrom.LOCAL_MEMORY

    def _cache_write_data(
            self,
            key: str,
            data: dict | list
        ) -> None:
        '''
            Cache write data
        '''
        self.cache_data[key] = {
            'data': data,
            'timestamp': datetime.now()
        }
