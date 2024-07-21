#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs Mini Cache.
#
# RLabs Mini Cache is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RLabs Mini Cache is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RLabs Mini Cache. If not, see <http://www.gnu.org/licenses/>.
#
'''
    Run Manual Test
    (entry point)

    For help type:
      poetry run manual-test-run --help

'''
import os
import logging
import time
from datetime import datetime
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


from rlabs_mini_cache.cache import Cache
from datetime import timedelta

MONGODB_USER = os.environ['MONGODB_USER']
MONGODB_PASS = os.environ['MONGODB_PASS']
MONGODB_CLUSTER_DOMAIN_NAME = os.environ['MONGODB_CLUSTER_DOMAIN_NAME']
MONGODB_APP_NAME = os.environ['MONGODB_APP_NAME']
MONGODB_URI = (
    f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_CLUSTER_DOMAIN_NAME}/"
    f"?appName={MONGODB_APP_NAME}&retryWrites=true&w=majority"
)

MONGODB_COLLECTION_NAME='rlabs_mini_cache_manual_test_run'

SAMPLE_JSON = {
    "a": 'the time is ' + datetime.now().time().strftime("%H:%M:%S"),
    "b": "2",
    "c": "3",
}

def data_read(
        key: str
    ):
    '''
        read
    '''
    return SAMPLE_JSON[key]

def data_read_slow(
        key: str
    ):
    '''
        read
    '''
    time.sleep(5)
    return SAMPLE_JSON[key]

def main():
    '''
        main
    '''
    # test_memory_backend()
    # test_file_backend()
    # test_file_slow_backend()
    test_mongodb_backend()


def test_file_backend():
    '''
        Test File Backend
    '''
    Cache.config(
        log_level=logging.DEBUG
    )

    cache = Cache.File(
        read_fn=data_read,
        max_age=timedelta(seconds=3),
        dir_path='../.cache'
    )

    print(
        #
        # this will be a cache miss
        # due to not being in cache
        #
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        #
        # this will be a cache miss
        # due to age
        #
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        cache.read('a')
    )

    cache.invalidate()

def test_file_slow_backend():
    '''
        Test File Slow Backend
    '''
    Cache.config(
        log_level=logging.DEBUG
    )

    cache = Cache.File(
        read_fn=data_read_slow,
        max_age=timedelta(seconds=60),
        dir_path='../.cache'
    )

    print(
        #
        # this will be a cache miss
        # due to not being in cache
        #
        # SLOW WAIT
        #
        cache.read('a')
    )

    #
    # anything here below
    # will be a cache hit: FAST
    #
    print(
        cache.read('a')
    )
    print(
        cache.read('a')
    )

    #
    # Write a new value
    #
    cache.write(
        'a', 'the time is ' + datetime.now().time().strftime("%H:%M:%S")
    )

    #
    # anything here below
    # will be a cache hit: FAST
    #
    print(
        cache.read('a')
    )
    print(
        cache.read('a')
    )

def test_memory_backend():
    '''
        Test Memory Backend
    '''
    Cache.config(
        log_level=logging.DEBUG
    )

    cache = Cache.Memory(
        read_fn=data_read,
        max_age=timedelta(seconds=3),
    )

    print(
        #
        # this will be a cache miss
        # due to not being in cache
        #
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        #
        # this will be a cache miss
        # due to age
        #
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        cache.read('a')
    )

def test_mongodb_backend():
    '''
        Test MongoDB Backend
    '''
    Cache.config(
        log_level=logging.DEBUG
    )

    mongodb_client = MongoClient(
        MONGODB_URI,
        server_api=ServerApi('1'),
        tlsCAFile=certifi.where()
    )

    cache = Cache.MongoDB(
        max_age=timedelta(seconds=4),
        mongodb_client=mongodb_client,
        mongodb_collection_unique_name=MONGODB_COLLECTION_NAME
    )

    cache.read_fn = data_read

    print(
        #
        # this will be a cache miss
        # due to not being in cache
        #
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        #
        # this will be a cache miss
        # due to age
        #
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        cache.read('a')
    )
    time.sleep(1.1)
    print(
        cache.read('a')
    )

    #cache.invalidate()
