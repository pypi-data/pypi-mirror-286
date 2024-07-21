#
# Copyright (C) 2024 RomanLabs, Rafael Roman Otero
# This file is part of RLabs Mini API.
#
# RLabs Mini API is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RLabs Mini API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RLabs Mini API. If not, see <http://www.gnu.org/licenses/>.
#
'''
    Run Manual Test
    (entry point)

    For help type:
      poetry run manual-test-run --help

'''
import os
import logging
from pathlib import Path

from rlabs_mini_api.request import GET
from rlabs_mini_api.request import POST
from rlabs_mini_api.request import DELETE
from rlabs_mini_api.request import PUT
from rlabs_mini_api.request import Request


GITLAB_API_URL = "https://gitlab.com/api/v4"
DUMMY_TEST_GROUP_ID = 79866152

def main():
    '''
        main
    '''

    ##
    ##  There's no main in a package, this is just a sample
    ##  for when building the classes
    ##
    ##  Replace this with a test
    ##

    # Configure for all requests
    Request.config(
        GITLAB_API_URL,
        { "PRIVATE-TOKEN": os.environ['TOKEN'] },
        retries=3,
        retry_base_delay=2.0,
        general_timeout=17.0,
        log_level=logging.DEBUG,
        response_log_dir=Path("../logs")
    )

    ## -- Delete variable --
    try:
        #
        # DELETE /groups/:id/variables/:key
        #
        DELETE                          \
            .groups                     \
            .id(DUMMY_TEST_GROUP_ID)    \
            .variables                  \
            .key("dummy_var")           \
            .exec()
    except Exception as e:
        if "404" in str(e):
            pass

    #
    # GET /groups/:id/variables?page=1&per_page=100
    #
    response = (GET
        .groups
        .id(DUMMY_TEST_GROUP_ID)
        .variables(page=1, per_page=100)
        .exec()
    )

    variables = (response.databox
        .map(
            lambda x: f"{x["key"]}={x["value"]}"
        )
        .to_json(
            indent=2
        )
        .data()
    )

    print(
        variables
    )


    # ## -- Create variable --
    #
    # POST /groups/:id/variables?key=dummy_var&value=dummy_val
    #
    POST                            \
        .groups                     \
        .id(DUMMY_TEST_GROUP_ID)    \
        .variables(
            key="dummy_var",
            value="dummy_val"
        )                           \
        .exec()

    #
    # GET /groups/:id/variables?page=1&per_page=100
    #
    response = (GET
        .groups
        .id(DUMMY_TEST_GROUP_ID)
        .variables(page=1, per_page=100)
        .exec()
    )

    variables = (response.databox
        .map(
            lambda x: f"{x["key"]}={x["value"]}"
        )
        .to_json(
            indent=2
        )
        .data()
    )

    print(
        variables
    )

    # ## -- Update variable --
    #
    # PUT /groups/:id/variables/:key
    #
    PUT(data={
        "value": "UPDATED_VALUE"
    })                              \
        .groups                     \
        .id(DUMMY_TEST_GROUP_ID)    \
        .variables                  \
        .key("dummy_var")           \
        .exec()

    #
    # GET /groups/:id/variables?page=1&per_page=100
    #
    response = (GET
        .groups
        .id(DUMMY_TEST_GROUP_ID)
        .variables(page=1, per_page=100)
        .exec()
    )

    variables = (response.databox
        .map(
            lambda x: f"{x["key"]}={x["value"]}"
        )
        .to_json(
            indent=2
        )
        .data()
    )

    print(
        variables
    )
