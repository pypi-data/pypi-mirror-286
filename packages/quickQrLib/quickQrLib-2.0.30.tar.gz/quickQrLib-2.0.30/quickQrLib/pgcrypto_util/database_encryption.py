from django.db import models
from django.conf import settings
from django.db.models import Func, Value

class AesEncrypt(Func):
    function = 'encrypt'
    template = "%(function)s(%(expressions)s, %(key)s::bytea, 'aes-256')"
    output_field = models.BinaryField()

    def __init__(self, expression, *args, **kwargs):
        key = kwargs.pop('key', settings.PGCRYPTO_KEY)
        super().__init__(expression, Value(key.encode('utf-8')), **kwargs)

class AesDecrypt(Func):
    function = 'decrypt'
    template = "%(function)s(%(expressions)s, %(key)s::bytea, 'aes-256')"
    output_field = models.TextField()

    def __init__(self, expression, *args, **kwargs):
        key = kwargs.pop('key', settings.PGCRYPTO_KEY)
        super().__init__(expression, Value(key.encode('utf-8')), **kwargs)
