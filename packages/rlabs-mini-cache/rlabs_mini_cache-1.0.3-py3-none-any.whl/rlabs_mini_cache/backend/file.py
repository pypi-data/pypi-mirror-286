'''
    File
'''
import os
from datetime import datetime
from typing import Callable
from datetime import timedelta
from pathlib import Path
from typing import cast
import json
from typing import Optional

from rlabs_mini_cache.backend.base import Backend
from rlabs_mini_cache.error import CacheMissNotFound
from rlabs_mini_cache.error import CacheFileNotFound
from rlabs_mini_cache.types import LoadedCache
from rlabs_mini_cache.types import ParsedJsonData
from rlabs_mini_cache.backend.utils.encoder import DateTimeEncoder
from rlabs_mini_cache.backend.utils.timestamp import parse_iso as timestamp_parse_iso
from rlabs_mini_cache.backend.utils.validate import top_level_fields as validate_top_level_fields
from rlabs_mini_cache.types import CacheEntry
from rlabs_mini_cache.backend.base import LoadedFrom

class File(Backend):
    '''
        File Backend
    '''
    CACHE_FILENAME: Path = Path('cache.json')

    def __init__(
            self,
            dir_path: Path,
            max_age: timedelta,
            read_fn: Optional[Callable[..., ParsedJsonData]] = None,
        ) -> None:
        '''
            Init
        '''
        self.cache_data: LoadedCache = {}
        self.cache_file_path: Path = dir_path / File.CACHE_FILENAME

        # create 'dir_path' if it doesn't exist
        os.makedirs(
            dir_path,
            exist_ok=True
        )

        super().__init__(
            max_age,
            self.__class__,
            read_fn
        )

    def _cache_init(
            self
        ) -> None:
        '''
            Cache init
        '''
        try:

            self.__load_cache()

        except CacheFileNotFound:

            self._cache_invalidate()

    def _cache_invalidate(
            self
    ) -> None:
        '''
            Cache invalidate
        '''
        self.cache_data = {}
        self.__commit_cache()

    def _cache_read_data(
            self,
            key: str
        ) -> ParsedJsonData:
        '''
            Cache read data
        '''
        if key not in self.cache_data:
            # data not in local cache
            raise CacheMissNotFound()   # trigger read from source

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
            Cache write
        '''
        self.cache_data[key] = CacheEntry(
            data=data,
            timestamp=datetime.now()
        )

        self.__commit_cache()


    def __load_cache(
            self
        ) -> None:
        '''
            Load cache from file
        '''
        #
        # Load
        #
        try:

            with open(
                self.cache_file_path,
                'r',
                encoding='utf-8'
            ) as file:

                try:
                    content = file.read().strip()

                    if content:
                        self.cache_data = json.loads(
                            content
                        )
                        Backend.logger.debug(
                            f"Loaded {len(self.cache_data)} entries from cache."
                        )

                    else:
                        Backend.logger.debug(
                            "Cache is empty."
                        )
                        self.cache_data = {}

                except json.JSONDecodeError as e:

                    Backend.logger.error(
                        f"Corrupted cache '{self.cache_file_path}' (failed to parse JSON). "
                        "Recovering by starting over with a fresh cache."
                    )
                    self.cache_data = {}

        except FileNotFoundError:
            raise CacheFileNotFound()

        #
        #   Validate and Parse ISO Timestamps
        #
        if self.cache_data:

            corrupted_keys = validate_top_level_fields(
                self.cache_data,
                str(self.cache_file_path),
                list(CacheEntry.__annotations__.keys()),
                Backend.logger
            )

            for key in corrupted_keys:
                # simply remove from loaded cache, it will be synced
                # to the cache file on next write
                del self.cache_data[key]

                Backend.logger.warning(
                    f"Deleted corrupted key '{key}' from cache."
                )

            timestamp_parse_iso(
                self.cache_data,
                str(self.cache_file_path),
                Backend.logger,
                delete_corrupted=True
            )


    def __commit_cache(
            self
        ) -> None:
        '''
            Commit cache to file
        '''
        with open(
            self.cache_file_path,
            'w',
            encoding='utf-8'
        ) as file:

            json.dump(
                self.cache_data,
                file,
                cls=DateTimeEncoder,
                indent=4
            )

        Backend.logger.debug(
            f"Committed {len(self.cache_data)} entries to cache."
        )

