import Crypto.Cipher.AES as AES
from Crypto import Random

key = Random.new().read(AES.block_size)
iv = Random.new().read(AES.block_size)
message = "Another message that is a factor of 16 bytes lon"
cbc_cypher = AES.new(key, mode=AES.MODE_CBC, IV=iv)
cyphertext = cbc_cypher.encrypt(message)
print(cyphertext)
plaintext = cbc_cypher.decrypt(cyphertext)
print(plaintext)
