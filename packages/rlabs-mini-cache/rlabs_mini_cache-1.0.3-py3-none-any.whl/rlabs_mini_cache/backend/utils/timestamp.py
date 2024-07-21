'''
    Timestamp
'''
import logging
from datetime import datetime
from typing import cast

from rlabs_mini_cache.backend.base import Backend
from rlabs_mini_cache.types import LoadedCache

def parse_iso(
        cache_data: LoadedCache,
        cache_id: str,
        logger: logging.Logger,
        delete_corrupted: bool = False,
    ) -> None:
    '''
        Parse ISO timestamp

        Parses all timestamp strings in loaded cache data. Assumes
        that the timestamp is in ISO 8601 format.

        When delete_corrupted=True and it finds a corrupted timestamp,
        it deletes the entryfrom the cache.

        Returns:
            The parsed timestamp
    '''
    corrupted_keys: list[str] = []

    for key, value in cache_data.items():
        try:
            value['timestamp'] = datetime.fromisoformat(
                cast(
                    str,
                    cache_data[key]['timestamp']
                )
            )
        except ValueError:
            logger.error(
                f"Corrupted cache entry in '{cache_id}'. Failed to parse timestamp  "
                f"for Key={key} (timestamp={cache_data[key]['timestamp']}). "
                f"Recovering by deleting the entry. Next read will continue as a cache miss."
            )
            corrupted_keys.append(key)

    if delete_corrupted:
        for key in corrupted_keys:
            del cache_data[key]
