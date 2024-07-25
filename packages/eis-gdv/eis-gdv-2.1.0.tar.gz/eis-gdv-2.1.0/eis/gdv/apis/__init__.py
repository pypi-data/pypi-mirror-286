
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from eis.gdv.api.mailbox_api import MailboxApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from eis.gdv.api.mailbox_api import MailboxApi
from eis.gdv.api.message_api import MessageApi
from eis.gdv.api.user_api import UserApi
from eis.gdv.api.vbas_api import VbasApi
from eis.gdv.api.vbu_api import VbuApi
from eis.gdv.api.zip_code_api import ZipCodeApi
from eis.gdv.api.default_api import DefaultApi
