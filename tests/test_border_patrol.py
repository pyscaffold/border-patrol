from border_patrol import with_print_stdout

import builtins
import logging
import re

import numpy as np
import sklearn

from border_patrol import BorderPatrol


def test_capture_import(bpatrol):
    report = bpatrol.report()
    assert len(report) > 1
    pkgs, _, _ = zip(*report)
    assert "numpy" in pkgs


def test_log_error(bpatrol, caplog):
    from border_patrol import with_log_error
    with caplog.at_level(logging.ERROR):
        bpatrol.at_exit()
        assert re.search("Following packages were imported:*", caplog.text)


def test_log_warning(bpatrol, caplog):
    from border_patrol import with_log_warning
    with caplog.at_level(logging.WARNING):
        bpatrol.at_exit()
        assert re.search("Following packages were imported:*", caplog.text)


def test_log_info(bpatrol, caplog):
    from border_patrol import with_log_info
    with caplog.at_level(logging.INFO):
        bpatrol.at_exit()
        assert re.search("Following packages were imported:*", caplog.text)


def test_log_debug(bpatrol, caplog):
    from border_patrol import with_log_debug
    with caplog.at_level(logging.INFO):
        bpatrol.at_exit()
        assert not re.search("Following packages were imported:*", caplog.text)
    with caplog.at_level(logging.DEBUG):
        bpatrol.at_exit()
        assert re.search("Following packages were imported:*", caplog.text)


def test_print_stderr(bpatrol, capsys):
    from border_patrol import with_print_stderr
    bpatrol.at_exit()
    stderr_out = capsys.readouterr().err
    assert re.search("Following packages were imported:*", stderr_out)


def test_dont_ignore_stdlib(bpatrol):
    bpatrol.ignore_std_lib = False
    report = bpatrol.report()
    assert len(report) > 1
    pkgs, _, _ = zip(*report)
    assert "os" in pkgs


def test_singleton_constructor(bpatrol):
    new_bpatrol = BorderPatrol()
    for attr in ("report_fun", "registered", "ignore_std_lib", "packages"):
        assert getattr(new_bpatrol, attr) == getattr(bpatrol, attr)
    before = bpatrol.ignore_std_lib
    BorderPatrol(ignore_std_lib=not before)
    assert bpatrol.ignore_std_lib is not before


def test_register(bpatrol):
    from border_patrol import builtin_import

    assert bpatrol.registered
    bpatrol.unregister()
    assert builtins.__import__ is builtin_import
    bpatrol.unregister()
    bpatrol.register()
    assert builtins.__import__ is bpatrol


def test_report_py(caplog):
    bpatrol = BorderPatrol(report_fun=logging.info, report_py=False)
    assert bpatrol.report_py is False
    with caplog.at_level(logging.INFO):
        bpatrol.at_exit()
    assert not re.search("Python version is", caplog.text)
    bpatrol.report_py = True
    with caplog.at_level(logging.INFO):
        bpatrol.at_exit()
    assert re.search("Python version is", caplog.text)
