##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Standard configuration errors
"""

import traceback

__all__ = [
    'ConfigurationError',
]

class ConfigurationError(Exception):
    """There was an error in a configuration
    """

    # A list of strings or things that can be converted to strings,
    # added by append_details as we walk back up the call/include stack.
    _details = ()

    def append_details(self, info):
        if isinstance(info, BaseException):
            info = traceback.format_exception_only(type(info), info)
            # Trim trailing newline
            info[-1] = info[-1].rstrip()
            self._details += tuple(info)
        else:
            self._details += (info,)
        return self

    def __str__(self):
        s = super(ConfigurationError, self).__str__()
        for i in self._details:
            s += '\n    ' + str(i)
        return s

    def __repr__(self):
        s = super(ConfigurationError, self).__repr__()
        for i in self._details:
            s += '\n    ' + repr(i)
        return s


class ConfigurationWrapperError(ConfigurationError):

    USE_INFO_REPR = False

    def __init__(self, info, exception):
        super(ConfigurationWrapperError, self).__init__(repr(info) if self.USE_INFO_REPR else info)
        self.append_details(exception)

        # This stuff is undocumented and not used but we store
        # for backwards compatibility
        self.info = info
        self.etype = type(exception)
        self.evalue = exception
