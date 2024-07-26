"""
Overview
========

**Summary:** Primary command-line interface (CLI) to fqr.

---

Usage
-----

```sh
$ fqr --help
```

"""

__all__ = (
    'cfg',
    'lib',
    'obj',
    'main',
    'utl',
    )

from . import cfg
from . import lib
from . import obj
from . import utl

from . utl import main
