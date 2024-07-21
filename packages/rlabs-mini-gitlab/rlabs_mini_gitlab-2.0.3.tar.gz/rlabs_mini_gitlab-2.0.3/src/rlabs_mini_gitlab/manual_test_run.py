#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs Mini Gitlab.
#
# RLabs Mini Gitlab is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RLabs Mini Gitlab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RLabs Mini Gitlab. If not, see <http://www.gnu.org/licenses/>.
#
'''
    Run Manual Test
    (entry point)

    For help type:
      poetry run manual-test-run --help

'''
from functools import wraps
import time
import os
from pathlib import Path
import logging
from datetime import timedelta
from rlabs_mini_cache.cache import Cache
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from rlabs_mini_gitlab.gitlab import Gitlab

GITLAB_API_V4_URL = "https://gitlab.com/api/v4"
TOKEN = os.environ['TOKEN']
TEST_GROUP_RLABS_MINI_GITLAB_ID = 88902018
TEST_GROUP_RLABS_MINI_GITLAB_TEST_PROJECT_ID = 58983879
TEST_GROUP_ID = TEST_GROUP_RLABS_MINI_GITLAB_ID
TEST_PROJECT_ID = TEST_GROUP_RLABS_MINI_GITLAB_TEST_PROJECT_ID
DUMMY_TEST_GROUP_ID = 88902018

MONGODB_USER = os.environ['MONGODB_USER']
MONGODB_PASS = os.environ['MONGODB_PASS']
MONGODB_CLUSTER_DOMAIN_NAME = os.environ['MONGODB_CLUSTER_DOMAIN_NAME']
MONGODB_APP_NAME = os.environ['MONGODB_APP_NAME']
MONGODB_URI = (
    f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_CLUSTER_DOMAIN_NAME}/"
    f"?appName={MONGODB_APP_NAME}&retryWrites=true&w=majority"
)

MONGODB_COLLECTION_NAME='rlabs_mini_gitlab_manual_test_run'


def main():
    '''
        main
    '''
    Cache.config(
        log_level=logging.DEBUG
    )

    cache = Cache.File(
        max_age=timedelta(days=1),   # 1 day
        dir_path='../.cache'
    )

    Gitlab.config(
        gitlab_url=GITLAB_API_V4_URL,
        gitlab_token=TOKEN,
        requests_general_timeout=11.0,
        mini_cache=cache,
        log_level=logging.DEBUG,
        response_log_dir=Path("../logs")
    )

    #
    #  GET /groups?per_page=1&page_num=X ALL PAGES
    #
    data = (Gitlab.GET
        .groups(per_page=1)
        .exec(
            fetch_all=True
        )
    )

    groups = (data
        .map(
            lambda x: x["name"]
        )
        .to_json(
            indent=2
        )
        .data()
    )

    print(groups)

