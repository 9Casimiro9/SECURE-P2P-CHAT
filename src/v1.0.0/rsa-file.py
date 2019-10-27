from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

key = RSA.generate(2048)
private_key = key.export_key()
file_out = open("private.pem", "wb")
file_out.write(private_key)

public_key = key.publickey().export_key()
file_out = open("public.pem", "wb")
file_out.write(public_key)

privKeyObj = RSA.importKey(private_key)
pubKeyObj =  RSA.importKey(public_key)

message = b'hello'

cipher = PKCS1_OAEP.new(pubKeyObj)
ciphertext = cipher.encrypt(message)

cipher = PKCS1_OAEP.new(privKeyObj)
message = cipher.decrypt(ciphertext)

print(ciphertext)

print(message.decode("utf-8"))