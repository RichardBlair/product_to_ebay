from .base import *

if DEBUG:
    try:
        from .dev import *
    except ImportError:
        print "Could not import dev.py. Please put dev.py into the settings module."
        sys.exit()
else:
    try:
        from .prod import *
    except ImportError:
        print "Could not import prod.py. Please put prod.py into the settings module."
        sys.exit()

try:
    from .private import *
except ImportError:
    print "Count not import private.py. Please put private.py into th settings module"
    sys.exit()
