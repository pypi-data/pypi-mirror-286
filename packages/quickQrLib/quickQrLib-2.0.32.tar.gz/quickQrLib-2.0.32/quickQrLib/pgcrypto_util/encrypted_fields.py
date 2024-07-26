from decimal import Decimal
from typing import Any
from django.db import models
from django.conf import settings
from django.db.models import Func, Value
from .database_encryption import AesEncrypt, AesDecrypt

class EncryptedTextField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.encrypt_key = settings.PGCRYPTO_KEY
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            return AesEncrypt(models.Value(value), self.encrypt_key)
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            return AesDecrypt(models.Value(value), self.encrypt_key)
        return value
    
    # def from_db_value(self, value, expression, connection):
    #     if value is not None:
    #         with connection.cursor() as cursor:
    #             cursor.execute(f"SELECT pgp_sym_decrypt(%s::bytea, %s)", [value, self.encrypt_key])
    #             return cursor.fetchone()[0]
    #     return value

    # def get_transform(self, lookup_name):
    #     if lookup_name == 'decrypt':
    #         return AesDecrypt
    #     return super().get_transform(lookup_name)

# Register the custom transform for the EncryptedTextField
models.TextField.register_lookup(AesDecrypt, 'decrypt')

class EncryptedCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.encrypt_key = settings.PGCRYPTO_KEY
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            return AesEncrypt(models.Value(value), self.encrypt_key)
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            return AesDecrypt(models.Value(value), self.encrypt_key)
        return value
    
    # def from_db_value(self, value, expression, connection):
    #     if value is not None:
    #         with connection.cursor() as cursor:
    #             cursor.execute(f"SELECT pgp_sym_decrypt(%s::bytea, %s)", [value, self.encrypt_key])
    #             return cursor.fetchone()[0]
    #     return value

    # def get_transform(self, lookup_name):
    #     if lookup_name == 'decrypt':
    #         return AesDecrypt
    #     return super().get_transform(lookup_name)
    
# Register the custom transform for the EncryptedCharField
models.CharField.register_lookup(AesDecrypt, 'decrypt')

class EncryptedEmailField(models.EmailField):
    def __init__(self, *args, **kwargs):
        self.encrypt_key = settings.PGCRYPTO_KEY
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            return AesEncrypt(models.Value(value), self.encrypt_key)
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            return AesDecrypt(models.Value(value), self.encrypt_key)
        return value
    
    # def from_db_value(self, value, expression, connection):
    #     if value is not None:
    #         with connection.cursor() as cursor:
    #             cursor.execute(f"SELECT pgp_sym_decrypt(%s::bytea, %s)", [value, self.encrypt_key])
    #             return cursor.fetchone()[0]
    #     return value

    # def get_transform(self, lookup_name):
    #     if lookup_name == 'decrypt':
    #         return AesDecrypt
    #     return super().get_transform(lookup_name)

# Register the custom transform for the EncryptedEmailField
models.EmailField.register_lookup(AesDecrypt, 'decrypt')

class EncryptedIntegerField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        self.encrypt_key = str(settings.PGCRYPTO_KEY)
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        # Convert the decrypted value to an integer
        decrypted_value = AesDecrypt(models.Value(value), self.encrypt_key)
        return int(decrypted_value)
        # return int(AesDecrypt(models.Value(value), self.encrypt_key))

    def get_prep_value(self, value):
        if value is None:
            return value
        # Convert integer to string for encryption
        value_str = str(value)
        return AesEncrypt(models.Value(value_str), self.encrypt_key)
        # return AesEncrypt(models.Value(str(value)), self.encrypt_key)

    # def get_transform(self, lookup_name):
    #     if lookup_name == 'decrypt':
    #         return AesDecrypt
    #     return super().get_transform(lookup_name)
    
# Register the custom transform for the EncryptedIntegerField
models.IntegerField.register_lookup(AesDecrypt, 'decrypt')

class EncryptedFloatField(models.FloatField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        # Convert the decrypted value to a float
        decrypted_value = AesDecrypt(models.Value(value), self.encrypt_key)
        return float(decrypted_value)
        # return float(AesDecrypt(models.Value(value), self.encrypt_key))

    def get_prep_value(self, value):
        if value is None:
            return value
        # Convert float to string for encryption
        value_str = str(value)
        return AesEncrypt(models.Value(value_str), self.encrypt_key)
        # return AesEncrypt(models.Value(str(value)), self.encrypt_key)

    # def get_transform(self, lookup_name):
    #     if lookup_name == 'decrypt':
    #         return AesDecrypt
    #     return super().get_transform(lookup_name)
    
# Register the custom transform for the EncryptedFloatField
models.FloatField.register_lookup(AesDecrypt, 'decrypt')

class EncryptedDecimalField(models.DecimalField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        # Convert the decrypted value to a decimal
        decrypted_value = AesDecrypt(models.Value(value), self.encrypt_key)
        return Decimal(decrypted_value)
        # return Decimal(AesDecrypt(models.Value(value), self.encrypt_key))

    def get_prep_value(self, value):
        if value is None:
            return value
        # Convert decimal to string for encryption
        value_str = str(value)
        return AesEncrypt(models.Value(value_str), self.encrypt_key)
        # return AesEncrypt(models.Value(str(value)), self.encrypt_key)

    # def get_transform(self, lookup_name):
    #     if lookup_name == 'decrypt':
    #         return AesDecrypt
    #     return super().get_transform(lookup_name)
    
# Register the custom transform for the EncryptedDecimalField
models.DecimalField.register_lookup(AesDecrypt, 'decrypt')

class EncryptedBooleanField(models.BooleanField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        # Convert the decrypted value to a boolean
        decrypted_value = AesDecrypt(models.Value(value), self.encrypt_key)
        return decrypted_value == 'True'
        # return AesDecrypt(models.Value(value), self.encrypt_key) == 'True'

    def get_prep_value(self, value):
        if value is None:
            return value
        # Convert boolean to string for encryption
        value_str = 'True' if value else 'False'
        return AesEncrypt(models.Value(value_str), self.encrypt_key)
        # return AesEncrypt(models.Value('True' if value else 'False'), self.encrypt_key)

    # def get_transform(self, lookup_name):
    #     if lookup_name == 'decrypt':
    #         return AesDecrypt
    #     return super().get_transform(lookup_name)
    
# Register the custom transform for the EncryptedBooleanField
models.BooleanField.register_lookup(AesDecrypt, 'decrypt')

class EncryptedGenericIPAddressField(models.GenericIPAddressField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return value
    
    def get_prep_value(self, value):
        if value is None:
            return value
        return AesEncrypt(models.Value(value), self.encrypt_key)
    
    # def get_transform(self, lookup_name):
    #     if lookup_name == 'decrypt':
    #         return AesDecrypt
    #     return super().get_transform(lookup_name)
    
# Register the custom transform for the EncryptedGenericIPAddressField
models.GenericIPAddressField.register_lookup(AesDecrypt, 'decrypt')