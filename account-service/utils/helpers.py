from cryptography.fernet import Fernet, InvalidToken
from decouple import config


class FernetCryptography:
    def __init__(self) -> None:
        key = config('FERNET_KEY')
        self.encryptor = Fernet(key)

    def encrypt(self, string: str) -> str:
        token = self.encryptor.encrypt(string.encode())
        return token.decode()

    def decrypt(self, string: str) -> bytes:
        try:
            decrypted_string = self.encryptor.decrypt(string)
        except InvalidToken:
            return None
        else: 
            return decrypted_string.decode()