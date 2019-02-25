import uuid

from django import forms
from django.db.models import Field, SubfieldBase
try:
    from django.utils.encoding import smart_unicode
except ImportError:
    from django.utils.encoding import smart_text as smart_unicode

try:
    # psycopg2 needs us to register the uuid type
    import psycopg2.extras
    psycopg2.extras.register_uuid()
except (ImportError, AttributeError):
    pass


class StringUUID(uuid.UUID):
    def __init__(self, *args, **kwargs):
        # get around UUID's immutable setter
        object.__setattr__(self, 'hyphenate', kwargs.pop('hyphenate', False))

        super(StringUUID, self).__init__(*args, **kwargs)

    def __str__(self):
        if self.hyphenate:
            return super(StringUUID, self).__str__()
        return self.hex

    def __len__(self):
        return len(self.__str__())

    # def __unicode__(self):
    #     if self.hyphenate:
    #         return super(StringUUID, self).__str__()
    #     return self.hex


class UUIDField(Field):
    """
    A field which stores a UUID value in hex format. This may also have the
    Boolean attribute 'auto' which will set the value on initial save to a new
    UUID value. Note that while all UUIDs are expected to be unique we enforce
    this with a DB constraint.
    """
    # TODO: support binary storage types
    __metaclass__ = SubfieldBase

    def __init__(self, version=4, node=None, clock_seq=None,
                 namespace=None, name=None, auto=False, hyphenate=False,
                 *args, **kwargs):
        assert version in (1, 3, 4, 5), "UUID version {ver}is not supported."\
            .format(ver=version)
        self.auto = auto
        self.version = version
        self.hyphenate = hyphenate

        if hyphenate:
            # We store UUIDs in string format, which is fixed at 36 characters.
            kwargs['max_length'] = 36
        else:
            # We store UUIDs in hex format, which is fixed at 32 characters.
            kwargs['max_length'] = 32

        if auto:
            # Do not let the user edit UUIDs if they are auto-assigned.
            kwargs['editable'] = False
            kwargs['blank'] = True
            kwargs['unique'] = True
        if version == 1:
            self.node, self.clock_seq = node, clock_seq
        elif version in (3, 5):
            self.namespace, self.name = namespace, name
        super(UUIDField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(UUIDField, self).deconstruct()
        del kwargs['max_length']

        if self.auto:
            kwargs.pop('editable')
            kwargs.pop('blank')
            kwargs.pop('unique')
            kwargs['auto'] = True

        if self.version != 4:
            kwargs['version'] = self.version
        if self.hyphenate:
            kwargs['hyphenate'] = self.hyphenate
        if hasattr(self, 'node') and self.node is not None:
            kwargs['node'] = self.node
        if hasattr(self, 'clock_seq') and self.clock_seq is not None:
            kwargs['clock_seq'] = self.clock_seq
        if hasattr(self, 'namespace') and self.namespace is not None:
            kwargs['namespace'] = self.namespace
        if hasattr(self, 'name') and self.name is not None:
            kwargs['name'] = self.name

        return name, path, args, kwargs

    def _create_uuid(self):
        if self.version == 1:
            args = (self.node, self.clock_seq)
        elif self.version in (3, 5):
            error = None
            if self.name is None:
                error_attr = 'name'
            elif self.namespace is None:
                error_attr = 'namespace'
            if error is not None:
                raise ValueError("The %s parameter of %s needs to be set." %
                                 (error_attr, self))
            if not isinstance(self.namespace, uuid.UUID):
                raise ValueError("The name parameter of %s must be an "
                                 "UUID instance." % self)
            args = (self.namespace, self.name)
        else:
            args = ()
        return getattr(uuid, 'uuid%s' % self.version)(*args)

    def db_type(self, connection=None):
        """
        Return the special uuid data type on Postgres databases.
        """
        if connection and 'postgres' in connection.vendor:
            return 'uuid'
        return 'char(%s)' % self.max_length

    def pre_save(self, model_instance, add):
        """
        This is used to ensure that we auto-set values if required.
        See CharField.pre_save
        """
        value = getattr(model_instance, self.attname, None)
        if self.auto and add and not value:
            # Assign a new value for this attribute if required.
            uuid = self._create_uuid()
            setattr(model_instance, self.attname, uuid)
            if self.hyphenate:
                value = uuid.__str__()
            else:
                value = uuid.hex
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        Casts uuid.UUID values into the format expected by the back end
        """
        if isinstance(value, uuid.UUID):
            value = str(value)
        if isinstance(value, str):
            if '-' in value:
                value = value.replace('-', '')
            uuid.UUID(value) # raises ValueError with invalid UUID format
        return value

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        if val is None:
            data = ''
        else:
            data = str(val)
        return data

    def to_python(self, value):
        """
        Returns a ``StringUUID`` instance from the value returned by the
        database. This doesn't use uuid.UUID directly for backwards
        compatibility, as ``StringUUID`` implements ``__unicode__`` with
        ``uuid.UUID.hex()``.
        """
        if not value:
            return None
        # attempt to parse a UUID including cases in which value is a UUID
        # instance already to be able to get our StringUUID in.
        return StringUUID(smart_unicode(value), hyphenate=self.hyphenate).__str__()

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.CharField,
            'max_length': self.max_length,
        }
        defaults.update(kwargs)
        return super(UUIDField, self).formfield(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [r"^uuidfield\.fields\.UUIDField"])
except ImportError:
    pass


