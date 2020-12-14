#!/usr/bin/env sh

#
# Copyright (c) The Diem Core Contributors
# SPDX-License-Identifier: Apache-2.0
#

pipenv run pytest -p vasp_validator.tests.plugin --pyargs vasp_validator.tests ./tests
