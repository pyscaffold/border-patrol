# -*- coding: utf-8 -*-
"""
Main module holding the actual functionality of Border-Patrol
"""
import atexit
import builtins
import inspect
import logging
import os.path
import sys
from builtins import __import__ as builtin_import
from operator import itemgetter

from pkg_resources import DistributionNotFound, get_distribution, working_set

UNKNOWN = "unknown"
BUILTINS = list(sys.builtin_module_names) + ["__future__"]

try:
    __version__ = get_distribution("border-patrol").version
except DistributionNotFound:
    __version__ = UNKNOWN

__file__ = os.path.join(
    os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe()))
)

logger = logging.getLogger(__name__)


class IdentityDict(dict):
    """Dictionary returning key by default"""

    def __missing__(self, key):
        return key


def get_pkg_to_dist_map():
    """Generates mapping of packages to distributions

    Returns:
        dict: mapping of packages to distributions
    """
    mapping = IdentityDict()
    for dist in working_set:
        try:
            pkgs = dist.get_metadata("top_level.txt")
        except Exception:
            pass
        else:
            for pkg in pkgs.split():
                mapping[pkg] = dist.project_name
    return mapping


def get_package(module):
    """Gets package part of module

    Args:
        module: module instance

    Returns:
        str: name of module's package
    """
    return module.__name__.split(".")[0]


def package_version(package, pkg_to_dist_map=None):
    """Retrieves version string of package

    Args:
        package (module): package as module instance
        pkg_to_dist_map (dict):
            mapping of packages to their distributions.
            Avoids recalculation if passed. (optional)

    Returns:
        str: version string of package
    """
    if pkg_to_dist_map is None:
        pkg_to_dist_map = get_pkg_to_dist_map()

    version = getattr(package, "__version__", UNKNOWN)
    if version == UNKNOWN:
        try:
            dist_name = pkg_to_dist_map[package.__name__]
            version = get_distribution(dist_name).version
        # Never fail and it's more than just DistributionNotFound
        except Exception:
            pass
    return version


def package_path(package):
    """Retrieves path of package

    Args:
        package: module instance of package

    Returns:
        str: path of package
    """
    path = getattr(package, "__file__", None)
    path = UNKNOWN if path is None else path
    return path


class BorderPatrol(object):
    """Border-Patrol singleton class to track imports of packages.

    Since BorderPatrol is a singleton, passing ``None`` for a value will
    keep the currently set value while passing a value will update the
    corresponding parameter.

    Args:
        report_fun (callable): output function for reporting imports
        ignore_std_lib (bool): ignore imports of Python's stdlib, default True
        report_py (bool): also report the Python runtime version, default True

    Attributes:
        template (str): string template for the report
    """

    # defines this class as singleton
    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.__init__(*args, **kwargs)
        return it

    def __init__(self, report_fun=None, ignore_std_lib=None, report_py=None):
        # retrieve following attributes from singleton instance if already set
        if report_fun is None:
            self.report_fun = getattr(self, "report_fun", logging.debug)
        else:
            self.report_fun = report_fun

        if ignore_std_lib is None:
            self.ignore_std_lib = getattr(self, "ignore_std_lib", True)
        else:
            self.ignore_std_lib = ignore_std_lib

        if report_py is None:
            self.report_py = getattr(self, "report_py", True)
        else:
            self.report_py = report_py

        self.registered = getattr(self, "registered", False)
        self.packages = getattr(self, "packages", [builtin_import(__name__)])
        self.template = getattr(self, "template", "{pkg}   {ver}   {path}")

    def __call__(self, *args, **kwargs):
        """Wraps the builtin import to track libraries"""
        module = builtin_import(*args, **kwargs)
        self.track(module)
        return module

    def track(self, module):
        """Tracks packages for later reporting

        Args:
            module: module instance
        """
        if module.__name__ in BUILTINS:
            return
        package = builtin_import(get_package(module))
        if package not in self.packages:
            self.packages.append(package)

    def register(self):
        """Registers/activates Border Patrol

        Returns:
            self: Border-Patrol instance
        """
        if not self.registered:
            builtins.__import__ = self
            atexit.register(self.at_exit)
            self.registered = True
        return self

    def unregister(self):
        """UnRegisters/deactivates Border Patrol

        Returns:
            self: Border-Patrol instance
        """
        if self.registered:
            builtins.__import__ = builtin_import
            atexit.unregister(self.at_exit)
            self.registered = False
        return self

    def report(self):
        """Reports currently imported libraries

        Returns:
            list: list of package's (name, version, path)
        """
        packages = self.packages
        pkg_to_dist_map = get_pkg_to_dist_map()
        if self.ignore_std_lib:
            packages = [
                package
                for package in packages
                if package.__name__ in pkg_to_dist_map.keys()
            ]

        return [
            (
                package.__name__,
                package_version(package, pkg_to_dist_map),
                package_path(package),
            )
            for package in packages
        ]

    def at_exit(self):
        """Handler to be called at exit"""
        self.report_fun(str(self))

    def __str__(self):
        msg = []
        if self.report_py:
            msg += ["Python version is {}".format(sys.version)]
        msg += ["Following packages were imported:"]
        report = self.report()
        names, versions, paths = zip(*report)
        name_just = max(len(name) for name in names)
        version_just = max(len(version) for version in versions)
        path_just = max(len(path) for path in paths)
        msg.append(
            self.template.format(
                pkg="PACKAGE".ljust(name_just),
                ver="VERSION".ljust(version_just),
                path="PATH".ljust(path_just),
            )
        )
        for name, version, path in sorted(report, key=itemgetter(0)):
            msg.append(
                self.template.format(
                    pkg=name.ljust(name_just),
                    ver=version.ljust(version_just),
                    path=path.ljust(path_just),
                )
            )
        return "\n".join(msg)
