# Library to aid
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from base64 import b64decode as b64d
from base64 import b64encode as b64e

# Main code
class Cryptography():
    '''
    A module dedicated to all cryptographic functions used by BKSchedule
    '''
    def _PBKDF2_hash(self, password, salt):
        '''
        Generate a SHA-512 PBKDF2 hash of length 32 to be used as AES key.

        Input data type:
        - `password`: `str`, arbitrary length
        - `salt`, `bytes`, preferably generated straight outta `os.urandom()`

        Output: 
        - `hash_`: `bytes`, the hash result
        '''
        hash_ = PBKDF2(password=password,
                     salt=salt,
                     dkLen=32, # Length restricted by AES-256
                     count=1000000,
                     hmac_hash_module=SHA512)
        return hash_

    def encrypt(self, data, password):
        '''
        Encrypt a given string with a password under AES (EAX mode).
        Salt used by default 2048 bits because why the fuck not.

        Input data type:
        - `data`: `str`, arbitrary length. In this case we prefer using 
        a JSON string (`json.dumps()`'s output).
        - `password`: `str`, arbitrary length.

        Output:
        - `result`: `dict` with the following KV pairs:
         - `encrypted_data`: `bytes`
         - `initial_state`: `dict`, containing information necessary to 
         reinitiate the cipher back to known sate for decrypt. States includes
         `nonce`, `salt` and `tag` stored as keys of the `initial_state` dict
        '''
        # Generate the salt from OS' designated source of randomness
        salt = os.urandom(2048)
        
        # Hash the password using PBKDF2-HMAC, SHA-512
        key = self._PBKDF2_hash(password, salt)
        
        # Initialize the cipher
        cipher = AES.new(key=key,
                         mode=AES.MODE_EAX)
        
        # Retrieve the nonce
        nonce = cipher.nonce
        
        # Encrypt the data
        encrypted_data, tag = cipher.encrypt_and_digest(data.encode())
        
        # Convert all data back to B64 for ease of storage
        result = {'encrypted_data': b64e(encrypted_data),
                  'initial_state': {
                      'nonce': b64e(nonce),
                      'salt': b64e(salt),
                      'tag': b64e(tag)
                  }
                 }
        return result
    
    def decrypt(self, password, encrypted_data, nonce, salt, tag):
        '''
        (Attempts to) Decrypt AES-encrypted data from a known cipher state.

        Input data type:
        - `key`: `str`, Base64-encoded. We will do the decode later.
        - `encrypted_data`, `nonce`, `salt`, `tag`: Same as above.

        Output:
        - `decrypted_data`: `bytes`

        Known exceptions:
        `ValueError`: Raised when decryption failed.
        '''
        # Decode all the B64 back to string
        encrypted_data,nonce,salt,tag = [b64d(i) for i in (encrypted_data,nonce,salt,tag)]
        
        # Retrieve the initial hash
        password = self._PBKDF2_hash(password, salt)
        
        # Initialize the cipher back the known state
        cipher = AES.new(key=password, mode=AES.MODE_EAX, nonce=nonce)
        
        # Decrypt:
        decrypted_data = cipher.decrypt_and_verify(encrypted_data, tag)
        return decrypted_data
