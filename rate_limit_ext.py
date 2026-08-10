"""Shared Flask-Limiter instance.

Defined app-less (standard Flask extension pattern) so blueprint modules can
attach ``@limiter.limit`` decorators without importing ``app`` (circular
import). ``app.py`` binds it to the application via ``limiter.init_app(app)``.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    # Sensitive endpoints keep explicit tighter limits; this default should not
    # block normal internal navigation and collection work.
    default_limits=["10000 per day", "1000 per hour"],
)
