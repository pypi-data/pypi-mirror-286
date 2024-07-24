import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class RSACryptoManager:

    def decrypt(self, data_encrypted, priv_key_pem):
        private_key = self.load_private_key(priv_key_pem)

        cipher = private_key
        data_encrypted = data_encrypted.replace('\r', '').replace('\n', '')
        key_size = (cipher.key_size + 7) // 8
        base64_block_size = (key_size // 3 * 4) if (key_size % 3 == 0) else (key_size // 3 * 4 + 4)
        iterations = len(data_encrypted) // base64_block_size
        decrypted_bytes = bytearray()

        for i in range(iterations):
            s_temp = data_encrypted[i * base64_block_size:(i + 1) * base64_block_size]
            b_temp = base64.b64decode(s_temp)
            b_temp = self.reverse(bytearray(b_temp))
            decrypted_chunk = private_key.decrypt(
                bytes(b_temp),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            decrypted_bytes.extend(decrypted_chunk)

        return decrypted_bytes.decode().strip()

    def encrypt(self, data_to_encrypt, pub_cer):
        public_key = self.load_public_key(pub_cer)

        cipher = public_key
        key_size = (cipher.key_size + 7) // 8
        max_length = key_size - 11
        bytes_to_encrypt = data_to_encrypt.encode()
        data_length = len(bytes_to_encrypt)
        iterations = (data_length + max_length - 1) // max_length
        encrypted_str = []

        for i in range(iterations):
            start = i * max_length
            end = min(start + max_length, data_length)
            chunk = bytes_to_encrypt[start:end]
            encrypted_bytes = cipher.encrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            reversed_bytes = self.reverse(bytearray(encrypted_bytes))
            encrypted_str.append(base64.b64encode(reversed_bytes).decode())

        # Join and clean the result
        encrypted_result = ''.join(encrypted_str)
        encrypted_result = encrypted_result.replace('\r', '').replace('\n', '')
        return encrypted_result

    def gen_rsa_key(self, key_size):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        public_key = private_key.public_key()

        private_key_der = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_key_der = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        private_key_str = self.der_to_string(private_key_der)
        public_key_str = self.der_to_string(public_key_der)

        return [public_key_str, private_key_str]

    def gen_key(self, key):
        if key is None:
            raise ValueError("key is null.")
        else:
            b_key_encoded = key.encode()  # Assuming key has an encode method
            rsa_key = self.der_to_string(b_key_encoded)
            return rsa_key

    def der_to_string(self, der_bytes):
        encoded = base64.b64encode(der_bytes).decode('utf-8')
        return '\n'.join(encoded[i:i + 64] for i in range(0, len(encoded), 64))

    def verify(self, data_to_verify, signed_data, pub_cer, is_file = False):
        public_key = self.load_public_key(pub_cer, is_file)
        signature = base64.b64decode(signed_data)
        try:
            public_key.verify(
                signature,
                data_to_verify.encode(),
                padding.PKCS1v15(),
                hashes.SHA512()
            )
            return True
        except Exception as e:
            return False

    def sign(self, data_to_sign: str, private_key: str, is_file: bool = False) -> str:
        _private_key = self.load_private_key(private_key, is_file)
        signature = _private_key.sign(
            data_to_sign.encode(),
            padding.PKCS1v15(),
            hashes.SHA512()
        )
        s_result = base64.b64encode(signature).decode()
        return s_result

    def fully_read_file(self, file_path: str) -> str:
        with open(file_path, 'r') as file:
            return file.read().strip()

    def load_private_key(self, key: str, is_file: bool = False) -> rsa.RSAPrivateKey:
        s_read_file = ""

        if is_file:
            s_read_file = self.fully_read_file(key)
        else:
            s_read_file = key.strip()

        if s_read_file.startswith("-----BEGIN PRIVATE KEY-----") and s_read_file.endswith("-----END PRIVATE KEY-----"):
            s_read_file = s_read_file.replace("-----BEGIN PRIVATE KEY-----", "")
            s_read_file = s_read_file.replace("-----END PRIVATE KEY-----", "")
            s_read_file = s_read_file.replace("\n", "")
            s_read_file = s_read_file.replace("\r", "")
            s_read_file = s_read_file.replace(" ", "")

        private_key = serialization.load_der_private_key(
            base64.b64decode(s_read_file),
            password=None,
            backend=default_backend()
        )

        return private_key

    def load_public_key(self, pub_cer: str, is_file: bool = False) -> rsa.RSAPublicKey:
        public_key = None

        try:
            if is_file:
                with open(pub_cer, 'rb') as file:
                    pub_cer = file.read()

            public_key = serialization.load_der_public_key(
                base64.b64decode(pub_cer),
                backend=default_backend()
            )
        except Exception as e:
            print(f"An error occurred: {e}")

        return public_key

    def encode_base64(data_to_encode):
        try:
            str_encoded = base64.b64encode(data_to_encode).decode('utf-8')
        except Exception as e:
            print(e)
            str_encoded = ""
        return str_encoded

    def decode_base64(data_to_decode):
        try:
            b_decoded = base64.b64decode(data_to_decode)
        except Exception as e:
            print(e)
            b_decoded = None
        return b_decoded

    def reverse(self, b):
        left = 0
        right = len(b) - 1
        while left < right:
            temp = b[left]
            b[left] = b[right]
            b[right] = temp
            left += 1
            right -= 1
        return b