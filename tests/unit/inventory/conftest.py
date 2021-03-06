#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest  # type: ignore[import]
import testlib

# TODO Orig conftest file (Python 2)
# If new fixtures are implemented, don't forget to port them to
#   tests-py3/unit/inventory/conftest.py


@pytest.fixture(scope="module")
def inventory_plugin_manager():
    return testlib.InventoryPluginManager()


@pytest.fixture(scope="module")
def check_manager():
    return testlib.CheckManager()
