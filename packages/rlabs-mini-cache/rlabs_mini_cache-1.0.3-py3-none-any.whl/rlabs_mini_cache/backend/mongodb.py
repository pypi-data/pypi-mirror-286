'''
    MongoDB
'''
from datetime import datetime
from typing import Callable
from typing import Any
from datetime import timedelta
from typing import cast
from pymongo.mongo_client import MongoClient
from typing import Optional

from rlabs_mini_cache.backend.base import Backend
from rlabs_mini_cache.error import CacheMissNotFound
from rlabs_mini_cache.types import ParsedJsonData
from rlabs_mini_cache.error import FailedToConnectToBackendError
from pymongo.collection import Collection
from rlabs_mini_cache.types import CacheEntry
from rlabs_mini_cache.types import LoadedCache
from rlabs_mini_cache.backend.utils.validate import top_level_fields as validate_top_level_fields
from rlabs_mini_cache.error import MongoDBEntryNotFoundError
from rlabs_mini_cache.error import FailedToDeleteCorruptedKeyError
from rlabs_mini_cache.backend.base import LoadedFrom

class MongoDB(Backend):
    '''
        MongoDB Backend
    '''
    CACHE_DB_NAME: str = 'romanlabs-mini-cache'
    CACHE_INDEX_FIELD_NAME: str = 'index'

    def __init__(
            self,
            mongodb_client: MongoClient,
            mongodb_collection_unique_name: str,    # apps have separate collections
                                                    # so deleting one doesn't affect the other
            max_age: timedelta,
            read_fn: Optional[Callable[..., ParsedJsonData]] = None,
        ) -> None:
        '''
            Init
        '''
        self.cache_data : LoadedCache = {}
        self.mongodb_client: MongoClient = mongodb_client
        self.mongodb_collection_name: str = mongodb_collection_unique_name
        self.mongodb_collection : Collection[Any] = cast(
            Collection[Any],
            None
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
        self.__mongodb_verify_connection(
            self.mongodb_client
        )
        self.mongodb_collection = self.__mongodb_init(
            self.mongodb_client,
            self.mongodb_collection_name,
            MongoDB.CACHE_DB_NAME,
            MongoDB.CACHE_INDEX_FIELD_NAME
        )


    def _cache_invalidate(
            self
    ) -> None:
        '''
            Cache invalidate
        '''
        self.cache_data = {}
        self.mongodb_collection.drop()

    def _cache_read_data(
            self,
            key: str
        ) -> ParsedJsonData:
        '''
            Cache read data
        '''
        if key not in self.cache_data:
            # data not in local cache
            try:
                # load from MongoDB
                self.__load_cache_entry(
                    key
                )
            except MongoDBEntryNotFoundError:
                # data not in MongoDB
                raise CacheMissNotFound()   # trigger read from source

        return self.cache_data[key]['data']

    def _cache_read_timestamp(
            self,
            key: str
        ) -> tuple[datetime, LoadedFrom]:
        '''
            Cache read timestamp
        '''
        if key in self.cache_data:

            return self.cache_data[key]['timestamp'], LoadedFrom.LOCAL_MEMORY

        else:
            # data not in local cache
            try:
                # load from MongoDB
                self.__load_cache_entry(
                    key
                )
            except MongoDBEntryNotFoundError:
                # data not in MongoDB
                raise CacheMissNotFound()   # trigger read from source

            return self.cache_data[key]['timestamp'], LoadedFrom.REMOTE_MONGODB

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

        self.__commit_entry_to_cache(
            key
        )

    def __load_cache_entry(
            self,
            key: str
        ) -> None:
        '''
            Load entry from MongoDB's collection 'self.mongodb_collection'. Loads
            the entry from MongoDB and stores it to 'self.cache_data[key]'.

            In MongoDB 'key' is stored as 'index'.

            Upon loading, the data is converted to CacheEntry

            E.g.:

                {
                    "index": key,   # <<<--- removed and used as key in python dict
                    "data": {
                        ...
                    }
                    "timestamp": "2021-10-10T22:07:00.000000"
                }

            becomes

                self.cache_data[key] = CacheEntry(
                    data={
                        ...
                    },
                    timestamp=datetime.datetime(2021, 10, 10, 22, 7)
                )


            Args:
                - key: The index/key to load

            Raises:
                MongoDBEntryNotFoundError if entry not found
        '''
        #
        # Load
        #
        document = self.mongodb_collection.find_one(
            {"index": key}
        )

        Backend.logger.debug(
            f"Loaded Document for index='{key}'"
        )

        if not document:
            raise MongoDBEntryNotFoundError()

        #
        # convert to CacheEntry
        #
        self.cache_data[key] = CacheEntry(
            data=document['data'],
            timestamp=document['timestamp']
        )

        #
        #   Validate
        #
        if self.cache_data:

            corrupted_keys = validate_top_level_fields(
                self.cache_data,
                self.mongodb_collection_name,
                list(CacheEntry.__annotations__.keys()),
                Backend.logger
            )

            self.__delete_corrupted_keys(
                self.mongodb_collection,
                self.cache_data,
                corrupted_keys
            )


    def __commit_entry_to_cache(
            self,
            key: str
        ) -> None:
        '''
            Commit entry to cache

            Upserts the loaded cache entry for 'key' to MongoDB's collection.
            'key' is stored as 'index' in the collection.

            Args:
                - key: The key/index to commit
        '''
        result = self.mongodb_collection.replace_one(
            {
                "index": key
            },
            {
                "index": key,
                "data": self.cache_data[key]['data'],
                "timestamp": self.cache_data[key]['timestamp']
            },
            upsert=True
        )

        if result.matched_count > 0:
            Backend.logger.debug(
                f"Replaced Document in Collection '{self.mongodb_collection_name}'"
            )
        else:
            Backend.logger.debug(
                f"Inserted new Document in Collection '{self.mongodb_collection_name}'")

        Backend.logger.debug(
            f"Committed 1 entry to cache: '{key}'"
        )

    def __mongodb_verify_connection(
            self,
            client: MongoClient
        ) -> None:
        '''
            Verify connection to MongoDB

            Args:
                mongodb_client: The MongoDB client

            Raises:
                FailedToConnectToBackendError if connection fails
        '''
        try:
            client.admin.command('ping')
        except Exception as e:
            raise FailedToConnectToBackendError(
                'MongoDB', str(e)
            ) from e

    def __mongodb_init(
            self,
            client: MongoClient,
            collection_name: str,
            db_name: str,
            index_field_name: str
        ) -> Collection[Any]:
        '''
            MongoDB Init

            Intializes MongoDB cache by creating a databse, collection
            and index.

            Args:
                - client: The MongoDB client
                - collection_name: The collection name
                - db_name: The database name
                - index_field_name: The index field name

            Returns:
                The MongoDB collection

        '''
        # Create DB and Collection (if not exists)
        collection = client[db_name][collection_name]
        Backend.logger.info(
            f"Connected to Collection '{collection_name}' in DB '{db_name}'"
        )

        # Create index
        index_name = collection.create_index(
            [(index_field_name, 1)],        # 1 for ascending order
            unique=True
        )
        Backend.logger.info(
            f"Created index: '{index_field_name}'"
        )

        return collection


    def __delete_corrupted_keys(
            self,
            collection: Collection[Any],
            cache_data: LoadedCache,
            keys: list[str]
        ) -> None:
        '''
            Delete corrupted keys from the loaded cache data 'cache_data' and
            MongoDB's collection 'collection'.

            Args:
                - collection: The MongoDB collection
                - cache_data: The loaded cache data
                - keys: The list of keys to delete

            Raises:
                FailedToDeleteCorruptedKeyError if deletion fails
        '''
        for key in keys:

            result = collection.delete_one(
                {"index": key}
            )

            if result.deleted_count > 0:
                Backend.logger.warning(
                    f"Deleted corrupted key '{key}' from cache (in MongoDB)."
                )
            else:
                raise FailedToDeleteCorruptedKeyError(
                    key
                )

            del cache_data[key]
