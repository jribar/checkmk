#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# pylint: disable=redefined-outer-name
import pytest  # type: ignore[import]

import shutil
import yaml

from cmk.utils import msi_patch

aaa_marker = "{AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA}".encode('ascii')


def test_parse_command_line():
    try:
        mode, f, param = msi_patch.parse_command_line(
            ["/path/to/executable", "mode", "msi", "param"])
    except Exception as _:
        assert False

    assert mode == "mode"
    assert f == "msi"
    assert param == "param"

    try:
        mode, f, param = msi_patch.parse_command_line(["/path/to/executable", "mode", "msi"])
    except Exception as _:
        assert False

    assert mode == "mode"
    assert f == "msi"
    assert param == ""

    try:
        msi_patch.parse_command_line(["/path/to/executable", "mode"])
        assert False
    except IndexError as _:
        assert True


def test_low_level_functions(conf_dir, cmk_dir):
    assert msi_patch.MSI_PACKAGE_CODE_OFFSET == 20
    assert msi_patch.MSI_PACKAGE_CODE_MARKER == "Intel;1033"
    assert msi_patch.generate_uuid() != msi_patch.generate_uuid()
    assert len(msi_patch.generate_uuid()) == 38
    p = conf_dir / "msi_state.yml"
    msi_patch.write_state_file(p, 12, "12")
    pos, id = msi_patch.load_state_file(p)
    assert pos == 12
    assert id == "12"


def test_patch_package_code_by_state_file(conf_dir, cmk_dir):
    # prepare file to tests
    if not cmk_dir.exists():
        pytest.skip("cmk_dir is not good")
    fname = u"test_bin.tst"
    src = cmk_dir / u"agents/wnx/test_files/msibuild/msi" / fname
    if not src.exists():
        pytest.skip("Path with MSI doesn't exist")

    uuid = msi_patch.generate_uuid()

    # prepare test file
    dst = conf_dir / fname
    shutil.copy(str(src), str(dst))
    base_content = dst.read_bytes()
    assert base_content.find(msi_patch.TRADITIONAL_UUID.encode('ascii')) != -1

    # patch 1, patching is successful
    p = conf_dir / "msi_state.yml"
    msi_patch.write_state_file(p, 4, msi_patch.TRADITIONAL_UUID)
    assert msi_patch.patch_package_code_by_state_file(f_name=dst, package_code=uuid, state_file=p)

    assert dst.stat().st_size == src.stat().st_size

    new_content = dst.read_bytes()
    assert new_content.find(uuid.encode('ascii')) == 4


def test_patch_package_code_with_state(conf_dir, cmk_dir):
    # prepare file to tests
    if not cmk_dir.exists():
        pytest.skip("cmk_dir is not good")
    fname = u"test_bin.tst"
    src = cmk_dir / u"agents/wnx/test_files/msibuild/msi" / fname
    if not src.exists():
        pytest.skip("Path with MSI doesn't exist")

    uuid = msi_patch.generate_uuid()

    # prepare test file
    dst = conf_dir / fname
    shutil.copy(str(src), str(dst))
    base_content = dst.read_bytes()
    assert base_content.find(msi_patch.TRADITIONAL_UUID.encode('ascii')) != -1

    # patch 1, patching is successful
    p = conf_dir / "msi_state.yml"
    assert msi_patch.patch_package_code(f_name=dst, package_code=uuid, state_file=p)

    assert dst.stat().st_size == src.stat().st_size

    new_content = dst.read_bytes()
    assert new_content.find(uuid.encode('ascii')) != -1

    pos, id_ = msi_patch.load_state_file(p)
    assert pos == 4
    assert id_ == uuid

    # prepare test file
    shutil.copy(str(src), str(dst))

    # patch 2, patching failed
    p = conf_dir / "msi_state.yml"
    assert not msi_patch.patch_package_code(
        f_name=dst, mask="asdyebdvdbee", package_code=uuid, state_file=p)

    assert dst.stat().st_size == src.stat().st_size

    new_content = dst.read_bytes()
    assert new_content.find(uuid.encode('ascii')) == -1

    yaml_content = p.read_bytes()
    state = yaml.safe_load(yaml_content)
    assert state is not None

    pos, id_ = msi_patch.load_state_file(p)
    assert pos == -1
    assert id_ == ""


def check_content(new_content, base_content, pos, uuid, marker):
    # type: (bytes, bytes, int, str, bytes) -> None
    assert new_content.find(marker) == -1
    new_pos = new_content.find(uuid.encode('ascii'))
    assert new_pos == pos
    assert new_content[pos:pos + len(uuid)] == uuid
    assert new_content[:pos] == base_content[:pos]
    assert new_content[pos + len(uuid):] == base_content[pos + len(uuid):]


def test_uuid():
    # relative random set of data, probably better to divide data in few arrays
    assert not msi_patch.valid_uuid("")
    assert not msi_patch.valid_uuid("1")
    assert msi_patch.valid_uuid("{80312934-35F7-11EA-A177-0800271CD485}")
    assert msi_patch.valid_uuid("{80312934-35F7-11EA-A177-0800271CD485}".lower())
    assert not msi_patch.valid_uuid("{80312934-35F7-11EA-A177-0800271CD_85}")
    assert not msi_patch.valid_uuid("{80312934-35F7-11EA-A177-0800271CDX85}")
    assert not msi_patch.valid_uuid("80312934-35F7-11EA-A177-0800271CDX85")
    assert not msi_patch.valid_uuid("DEFADEFADEFA")


def test_uuid_base():
    assert "{21fac8ef-8042-50ca-8c85-fbca566e726e}".upper() == msi_patch.generate_uuid_from_base(
        "012")


def test_patch_package_code_by_marker(conf_dir, cmk_dir):
    # prepare file to tests
    if not cmk_dir.exists():
        pytest.skip("cmk_dir is not good")
    fname = u"test_bin.tst"
    src = cmk_dir / u"agents/wnx/test_files/msibuild/msi" / fname
    if not src.exists():
        pytest.skip("Path with MSI doesn't exist")

    uuid = msi_patch.generate_uuid()

    # prepare test file
    dst = conf_dir / fname
    shutil.copy(str(src), str(dst))
    base_content = dst.read_bytes()
    assert base_content.find(msi_patch.TRADITIONAL_UUID.encode('ascii')) != -1

    # patch 1
    pos = base_content.find(aaa_marker)
    assert pos != -1
    assert msi_patch.patch_package_code_by_marker(f_name=dst, package_code=uuid)

    new_content = dst.read_bytes()
    check_content(new_content=new_content,
                  base_content=base_content,
                  pos=pos,
                  uuid=uuid,
                  marker=aaa_marker)

    # prepare test file
    shutil.copy(str(src), str(dst))

    # patch 2
    st_f = conf_dir / "state_file_2.yml"
    assert msi_patch.patch_package_code_by_marker(f_name=dst, package_code=uuid, state_file=st_f)

    new_content = dst.read_bytes()
    loc = new_content.find(uuid.encode('ascii'))
    pos, id = msi_patch.load_state_file(st_f)
    assert loc == pos
    assert id == uuid


def test_patch_package_code(conf_dir, cmk_dir):
    # prepare file to tests
    if not cmk_dir.exists():
        pytest.skip("cmk_dir is not good")
    fname = u"test_bin.tst"
    src = cmk_dir / u"agents/wnx/test_files/msibuild/msi" / fname
    if not src.exists():
        pytest.skip("Path with MSI doesn't exist")

    uuid = msi_patch.generate_uuid()
    marker = msi_patch.TRADITIONAL_UUID.encode('ascii')

    # prepare test file
    dst = conf_dir / fname
    shutil.copy(str(src), str(dst))
    base_content = dst.read_bytes()
    pos = base_content.find(marker)
    assert pos != -1

    # patch 1, default
    assert msi_patch.patch_package_code(f_name=dst, mask="", package_code=uuid)

    new_content = dst.read_bytes()
    check_content(new_content=new_content,
                  base_content=base_content,
                  pos=pos,
                  uuid=uuid,
                  marker=marker)

    # prepare test file
    shutil.copy(str(src), str(dst))
    # patch 2
    uuid = msi_patch.generate_uuid()
    assert msi_patch.patch_package_code(f_name=dst,
                                        mask=msi_patch.TRADITIONAL_UUID,
                                        package_code=uuid)

    new_content = dst.read_bytes()
    check_content(new_content=new_content,
                  base_content=base_content,
                  pos=pos,
                  uuid=uuid,
                  marker=marker)

    # prepare test file
    shutil.copy(str(src), str(dst))
    # patch 3, mask is absent
    assert not msi_patch.patch_package_code(f_name=dst, mask="Cant/Be/Found/In")

    new_content = dst.read_bytes()
    assert new_content.find(marker) != -1
