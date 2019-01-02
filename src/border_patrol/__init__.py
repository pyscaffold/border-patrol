# -*- coding: utf-8 -*-
import sys
import os.path
import inspect
import atexit
import logging
import builtins
from operator import itemgetter
from builtins import __import__ as builtin_import
from pkg_resources import get_distribution, DistributionNotFound, working_set

UNKNOWN = 'unknown'
BUILTINS = list(sys.builtin_module_names) + ['__future__']

try:
    __version__ = get_distribution('border-patrol').version
except DistributionNotFound:
    __version__ = UNKNOWN

__file__ = os.path.join(
    os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe())))


class DefaultDict(dict):
    def __missing__(self, key):
        return key


def get_pkg_to_dist_map():
    """Generates Mapping of packages to distributions
    """
    mapping = DefaultDict()
    for dist in working_set:
        try:
            pkgs = dist.get_metadata('top_level.txt')
        except:
            pass
        else:
            for pkg in pkgs.split():
                mapping[pkg] = dist.project_name
    return mapping


def get_package(package):
    return package.__name__.split('.')[0]


def package_name(package):
    return package.__name__


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
        except:  # Never fail and it's more than just DistributionNotFound
            pass
    return version


def package_path(package):
    return getattr(package, "__file__", UNKNOWN)


class BorderPatrol(object):
    # Define this class as singleton
    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.__init__(*args, **kwargs)
        return it

    def __init__(self, report_fun=None, ignore_std_lib=None):
        # retrieve following attributes from singleton instance if already set
        if report_fun is None:
            self.report_fun = getattr(self, 'report_fun', logging.debug)
        else:
            self.report_fun = report_fun

        if ignore_std_lib is None:
            self.ignore_std_lib = getattr(self, 'ignore_std_lib', True)
        else:
            self.ignore_std_lib = ignore_std_lib

        self.registered = getattr(self, 'registered', False)
        self.packages = getattr(self, 'packages', [builtin_import(__name__)])

    def __call__(self, *args, **kwargs):
        module = builtin_import(*args, **kwargs)
        self.track(module)
        return module

    def track(self, module):
        if module.__name__ in BUILTINS:
            return
        package = builtin_import(get_package(module))
        if package not in self.packages:
            self.packages.append(package)

    def register(self):
        if not self.registered:
            builtins.__import__ = self
            atexit.register(self.at_exit)
            self.registered = True
        return self

    def unregister(self):
        if self.registered:
            builtins.__import__ = builtin_import
            atexit.unregister(self.at_exit)
            self.registered = False
        return self

    def report(self):
        packages = self.packages
        pkg_to_dist_map = get_pkg_to_dist_map()
        if self.ignore_std_lib:
            packages = [package for package in packages
                        if package.__name__ in pkg_to_dist_map.keys()]

        return [(package_name(package),
                 package_version(package, pkg_to_dist_map),
                 package_path(package))
                for package in packages]

    def __repr__(self):
        return str(self.report())

    def at_exit(self):
        self.report_fun(str(self))

    def __str__(self):
        msg = ["Python version is {}".format(sys.version)]
        msg += ["Following modules were imported:"]
        template = "{}   {}   {}"

        report = self.report()
        names, versions, paths = zip(*report)
        name_just = max(len(name) for name in names)
        version_just = max(len(version) for version in versions)
        path_just = max(len(path) for path in paths)
        msg.append(template.format(
            'PACKAGE'.ljust(name_just),
            'VERSION'.ljust(version_just),
            'PATH'.ljust(path_just)
            ))
        for row in sorted(report, key=itemgetter(0)):
            name, version, path = row
            msg.append(template.format(
                name.ljust(name_just),
                version.ljust(version_just),
                path.ljust(path_just)
                ))
        return '\n'.join(msg)
