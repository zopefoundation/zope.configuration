##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""Configuration-specific schema fields
"""
import os
import sys
import warnings

from zope.interface import implementer
from zope.schema import Bool as schema_Bool
from zope.schema import DottedName
from zope.schema import Field
from zope.schema import InterfaceField
from zope.schema import List
from zope.schema import PythonIdentifier as schema_PythonIdentifier
from zope.schema import Text
from zope.schema import ValidationError
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import InvalidValue

from zope.configuration.exceptions import ConfigurationError
from zope.configuration.interfaces import InvalidToken


class PythonIdentifier(schema_PythonIdentifier):
    """
    This class is like `zope.schema.PythonIdentifier`, but does not allow empty strings.
    """

    def _validate(self, value):
        super(PythonIdentifier, self)._validate(value)
        if not value:
            raise ValidationError(value).with_field_and_value(self, value)


@implementer(IFromUnicode)
class GlobalObject(Field):
    """
    An object that can be accessed as a module global.

    The special value ``*`` indicates a value of `None`; this is
    not validated against the *value_type*.
    """

    _DOT_VALIDATOR = DottedName()

    def __init__(self, value_type=None, **kw):
        self.value_type = value_type
        super(GlobalObject, self).__init__(**kw)

    def _validate(self, value):
        super(GlobalObject, self)._validate(value)
        if self.value_type is not None:
            self.value_type.validate(value)

    def fromUnicode(self, value):
        name = str(value.strip())

        # special case, mostly for interfaces
        if name == '*':
            return None

        try:
            # Leading dots are allowed here to indicate current
            # package.
            to_validate = name[1:] if name.startswith('.') else name
            self._DOT_VALIDATOR.validate(to_validate)
        except ValidationError as v:
            v.with_field_and_value(self, name)
            raise

        try:
            value = self.context.resolve(name)
        except ConfigurationError as v:
            raise ValidationError(v).with_field_and_value(self, name)

        self.validate(value)
        return value


@implementer(IFromUnicode)
class GlobalInterface(GlobalObject):
    """An interface that can be accessed from a module.
    """
    def __init__(self, **kw):
        super(GlobalInterface, self).__init__(InterfaceField(), **kw)


@implementer(IFromUnicode)
class Tokens(List):
    """A list that can be read from a space-separated string.
    """
    def fromUnicode(self, u):
        u = u.strip()
        if u:
            vt = self.value_type.bind(self.context)
            values = []
            for s in u.split():
                try:
                    v = vt.fromUnicode(s)
                except ValidationError as v:
                    raise InvalidToken("%s in %s" % (v, u)).with_field_and_value(self, s)
                else:
                    values.append(v)
        else:
            values = []

        self.validate(values)

        return values


@implementer(IFromUnicode)
class Path(Text):
    """A file path name, which may be input as a relative path

    Input paths are converted to absolute paths and normalized.
    """
    def fromUnicode(self, u):
        u = u.strip()
        if os.path.isabs(u):
            return os.path.normpath(u)

        return self.context.path(u)


@implementer(IFromUnicode)
class Bool(schema_Bool):
    """A boolean value

    Values may be input (in upper or lower case) as any of:
       yes, no, y, n, true, false, t, or f.
    """
    def fromUnicode(self, value):
        value = value.lower()
        if value in ('1', 'true', 'yes', 't', 'y'):
            return True
        if value in ('0', 'false', 'no', 'f', 'n'):
            return False
        # Unlike the superclass, anything else is invalid.
        raise InvalidValue().with_field_and_value(self, value)



@implementer(IFromUnicode)
class MessageID(Text):
    """Text string that should be translated.

    When a string is converted to a message ID, it is also
    recorded in the context.
    """

    __factories = {}

    def fromUnicode(self, u):
        context = self.context
        domain = getattr(context, 'i18n_domain', '')
        if not domain:
            domain = 'untranslated'
            warnings.warn(
                "You did not specify an i18n translation domain for the "\
                "'%s' field in %s" % (self.getName(), context.info.file )
                )
        if not isinstance(domain, str):
            # IZopeConfigure specifies i18n_domain as a BytesLine, but that's
            # wrong on Python 3, where the filesystem uses str, and hence
            # zope.i18n registers ITranslationDomain utilities with str names.
            # If we keep bytes, we can't find those utilities.
            enc = sys.getfilesystemencoding() or sys.getdefaultencoding()
            domain = domain.decode(enc)

        v = super(MessageID, self).fromUnicode(u)

        # Check whether there is an explicit message is specified
        default = None
        if v.startswith('[]'):
            v = v[2:].lstrip()
        elif v.startswith('['):
            end = v.find(']')
            default = v[end+2:]
            v = v[1:end]

        # Convert to a message id, importing the factory, if necessary
        factory = self.__factories.get(domain)
        if factory is None:
            import zope.i18nmessageid
            factory = zope.i18nmessageid.MessageFactory(domain)
            self.__factories[domain] = factory

        msgid = factory(v, default)

        # Record the string we got for the domain
        i18n_strings = context.i18n_strings
        strings = i18n_strings.get(domain)
        if strings is None:
            strings = i18n_strings[domain] = {}
        locations = strings.setdefault(msgid, [])
        locations.append((context.info.file, context.info.line))

        return msgid
