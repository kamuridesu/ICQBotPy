try:
    from dispatcher import Dispatcher
    from ICQBot import ICQBot
except ImportError:
    from .dispatcher import Dispatcher
    from .ICQBot import ICQBot
