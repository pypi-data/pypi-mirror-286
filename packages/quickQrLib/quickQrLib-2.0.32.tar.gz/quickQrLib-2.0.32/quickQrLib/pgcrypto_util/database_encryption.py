from django.db import models
from django.conf import settings
from django.db.models import Func, Value

class AesEncrypt(Func):
    function = 'pgp_sym_encrypt'
    template = "%(function)s(%(expressions)s, '%(key)s', 'cipher-algo=aes256')"

    def __init__(self, expression, key, **extra):
        super().__init__(expression, **extra)
        self.extra['key'] = key

class AesDecrypt(Func):
    function = 'pgp_sym_decrypt'
    template = "%(function)s(%(expressions)s, '%(key)s')"

    def __init__(self, expression, key, **extra):
        super().__init__(expression, **extra)
        self.extra['key'] = key
