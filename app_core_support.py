"""Generic app-core utilities used by the main Flask application."""

from threading import Lock

from flask import session


class LazyServiceProxy:
    """Lazy-initialize expensive services only when a route actually needs them."""

    def __init__(self, factory, label):
        self._factory = factory
        self._label = label
        self._instance = None
        self._initialized = False
        self._lock = Lock()

    def _get_instance(self):
        if self._initialized:
            return self._instance

        with self._lock:
            if self._initialized:
                return self._instance
            self._instance = self._factory()
            self._initialized = True
            return self._instance

    @property
    def available(self):
        instance = self._get_instance()
        return bool(instance and getattr(instance, 'available', False))

    @property
    def initialized(self):
        return self._initialized

    def reset(self):
        with self._lock:
            self._instance = None
            self._initialized = False

    def __bool__(self):
        return self.available

    def __getattr__(self, name):
        instance = self._get_instance()
        if instance is None:
            raise AttributeError(f"{self._label} is unavailable")
        return getattr(instance, name)


class LazyLoadedDict(dict):
    """Dictionary that defers loading until first access."""

    def __init__(self, loader, label):
        super().__init__()
        self._loader = loader
        self._label = label
        self._loaded = False
        self._load_lock = Lock()

    def _ensure_loaded(self):
        if self._loaded:
            return

        with self._load_lock:
            if self._loaded:
                return

            data = self._loader() or {}
            if not isinstance(data, dict):
                raise TypeError(f"{self._label} loader must return a dict")

            dict.clear(self)
            dict.update(self, data)
            self._loaded = True

    def refresh(self):
        """Force a reload on the next access and return the refreshed mapping."""
        with self._load_lock:
            self._loaded = False
            dict.clear(self)
        self._ensure_loaded()
        return self

    def __getitem__(self, key):
        self._ensure_loaded()
        return dict.__getitem__(self, key)

    def get(self, key, default=None):
        self._ensure_loaded()
        return dict.get(self, key, default)

    def items(self):
        self._ensure_loaded()
        return dict.items(self)

    def keys(self):
        self._ensure_loaded()
        return dict.keys(self)

    def values(self):
        self._ensure_loaded()
        return dict.values(self)

    def __iter__(self):
        self._ensure_loaded()
        return dict.__iter__(self)

    def __len__(self):
        self._ensure_loaded()
        return dict.__len__(self)

    def __contains__(self, key):
        self._ensure_loaded()
        return dict.__contains__(self, key)

    def copy(self):
        self._ensure_loaded()
        return dict.copy(self)

    def __bool__(self):
        return bool(len(self))

    def __setitem__(self, key, value):
        self._ensure_loaded()
        dict.__setitem__(self, key, value)

    def update(self, *args, **kwargs):
        self._ensure_loaded()
        dict.update(self, *args, **kwargs)

    def clear(self):
        self._ensure_loaded()
        dict.clear(self)

    def pop(self, key, default=None):
        self._ensure_loaded()
        return dict.pop(self, key, default)

    def popitem(self):
        self._ensure_loaded()
        return dict.popitem(self)

    def setdefault(self, key, default=None):
        self._ensure_loaded()
        return dict.setdefault(self, key, default)


def current_user_is_admin():
    """Return True when the current session belongs to an admin-level user
    (admin or direktor — the director has full admin parity)."""
    return session.get('user_role') in ('admin', 'direktor') or session.get('is_admin', False)


def can_access_owned_record(owner_email, user_email, user_role):
    """Allow record access to the owner or an admin-level user."""
    return user_role in ('admin', 'direktor') or (owner_email and owner_email == user_email)
