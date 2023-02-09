from django.utils.http import urlsafe_base64_encode
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings




class FernetCryptography:
    def __init__(self) -> None:
        key = urlsafe_base64_encode(settings.SECRET_KEY)
        self.encryptor = Fernet(key)

    @classmethod
    def fernet_encryption(cls, string: str) -> str:
        token = cls.encryptor.encrypt(string.encode())
        return token

    def fernet_decryption(cls, string: str) -> bytes:
        try:
            decrypted_string = cls.encryptor.decrypt(string.encode())
        except InvalidToken:
            return None
        else: 
            return decrypted_string.decode()