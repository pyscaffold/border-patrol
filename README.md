[![ReadTheDocs](https://readthedocs.org/projects/border-patrol/badge/?version=latest)](https://border-patrol.readthedocs.io/en/latest/?badge=latest)
[![Coveralls](https://img.shields.io/coveralls/github/pyscaffold/border-patrol/master.svg)](https://coveralls.io/r/pyscaffold/border-patrol)
[![PyPI-Server](https://img.shields.io/pypi/v/border-patrol.svg)](https://pypi.org/project/border-patrol/)    

# Border-Patrol 

Border-Patrol logs all imported packages and their version to support you while debugging. In 95% of all cases when
something suddenly breaks in production it is due to some different version in one of your requirements. Pinning down the
versions of all your dependencies and dependencies of dependencies inside a virtual environments helps you to overcome
this problem but is quite cumbersome and thus this method is not always applied in practice.

With Border-Patrol you can easily find the culprit by looking in the logs of the last working versions and compare it
to the failing one since Border-Patrol will list all imported packages and their corresponding version right at the
end of your application.


## Usage

Border-Patrol is really simple to use, just install it with `pip install border-patrol` 
and import it before any other package, e.g.:
```python
from border_patrol import with_print

import numpy as np
import scipy as sp
import sklearn
```
If you run those lines in a script, you will get the a similar output to this one:
```console
Python version is 3.6.7 |Anaconda, Inc.| (default, Oct 23 2018, 14:01:38) 
[GCC 4.2.1 Compatible Clang 4.0.1 (tags/RELEASE_401/final)]
Following modules were imported:
PACKAGE         VERSION                         PATH                                                                                     
border_patrol   0.0.post0.dev1+g32fe77c.dirty   /Users/fwilhelm/Sources/border_patrol/src/border_patrol                                  
numpy           1.15.1                          /Users/fwilhelm/anaconda/envs/recsys_data/lib/python3.6/site-packages/numpy/__init__.py  
scipy           1.1.0                           /Users/fwilhelm/anaconda/envs/recsys_data/lib/python3.6/site-packages/scipy/__init__.py  
sklearn         0.19.2                          /Users/fwilhelm/anaconda/envs/recsys_data/lib/python3.6/site-packages/sklearn/__init__.py
```

If you import `with_print`, Border-Patrol will use `print` as output function. Since most production applications
will rather use the `logging` module, you can tell Border-Patrol to use it by importing `with_log_{error|warning|info|debug}`.
For instance `from border_patrol import with_log_info` will log the final report by using the `INFO` logging level.

If you want even more fine grained control you can import the `BorderPatrol` class directly from the `border_patrol` package
and use the `register()` and `unregister()` method to activate and deactivate it, respectively. 


## How does it work?

Border-Patrol is actually quite simple. It overwrites the `__import__` function in Python's `builtins` package to track
every imported package. Additionally it registers an *atexit* handler to be called when your application finishes and
reports all imported modules. To avoid any problem registering these things more than once, Border-Patrol is implemented
as Singleton and thus it is *not* thread-safe. 


## Note

This project has been set up using PyScaffold 3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
