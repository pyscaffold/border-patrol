from border_patrol import with_print_stdout
import re
import sys
import builtins
import logging

import numpy as np
import sklearn


def test_capture_import(border_patrol):
    report = border_patrol.report()
    assert len(report) > 1
    pkgs, _, _ = zip(*report)
    assert 'numpy' in pkgs


def test_log_error(border_patrol, caplog):
    from border_patrol import with_log_error
    with caplog.at_level(logging.ERROR):
        border_patrol.at_exit()
        assert re.search("Following packages were imported:*", caplog.text)


def test_log_warning(border_patrol, caplog):
    from border_patrol import with_log_warning
    with caplog.at_level(logging.WARNING):
        border_patrol.at_exit()
        assert re.search("Following packages were imported:*", caplog.text)


def test_log_info(border_patrol, caplog):
    from border_patrol import with_log_info
    with caplog.at_level(logging.INFO):
        border_patrol.at_exit()
        assert re.search("Following packages were imported:*", caplog.text)


def test_log_debug(border_patrol, caplog):
    from border_patrol import with_log_debug
    with caplog.at_level(logging.INFO):
        border_patrol.at_exit()
        assert not re.search("Following packages were imported:*", caplog.text)
    with caplog.at_level(logging.DEBUG):
        border_patrol.at_exit()
        assert re.search("Following packages were imported:*", caplog.text)


def test_print_stderr(border_patrol, capsys):
    from border_patrol import with_print_stderr
    border_patrol.at_exit()
    stderr_out = capsys.readouterr().err
    assert re.search("Following packages were imported:*", stderr_out)


def test_dont_ignore_stdlib(border_patrol):
    border_patrol.ignore_std_lib = False
    report = border_patrol.report()
    assert len(report) > 1
    pkgs, _, _ = zip(*report)
    assert 'os' in pkgs


def test_singleton_constructor(border_patrol):
    from border_patrol import BorderPatrol
    new_border_patrol = BorderPatrol()
    for attr in ('report_fun', 'registered', 'ignore_std_lib', 'packages'):
        assert getattr(new_border_patrol, attr) == getattr(border_patrol, attr)
    before = getattr(border_patrol, 'ignore_std_lib')
    new_border_patrol = BorderPatrol(ignore_std_lib=not before)
    assert border_patrol.ignore_std_lib is not before


def test_register(border_patrol):
    from border_patrol import builtin_import
    assert border_patrol.registered
    border_patrol.unregister()
    assert builtins.__import__ is builtin_import
    border_patrol.unregister()
    border_patrol.register()
    assert builtins.__import__ is border_patrol
