from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA3_256 
import time


def aes_encrypt_block(key, block):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(block)

def tdm_hash(message, key1, key2, iv, block_size=128):
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    padded_message = pad(message, block_size)
    blocks = [padded_message[i:i+block_size] for i in range(0, len(padded_message), block_size)]
    
    H = iv
    G = iv
    
    for block in blocks:
        prev_H = H
        prev_G = G

        H = aes_encrypt_block(key1, block)
        H = bytes(a^b for a,b in zip(H, prev_H))

        G = aes_encrypt_block(key2, block)
        G = bytes(a^b for a,b in zip(G, prev_G))
    
    out = H + G
    return out


message_sizes = [100, 1000, 5000, 10000]
key1 = b'This is a key123'
key2 = b'This is a key456'
iv = b'This is an IV456'


for size in message_sizes:
    size = size*1000
    message = b'a' * size

    print(f"Nachrichtengröße: {size} Bytes")
    start_time = time.time()
    tdm_hash_value = tdm_hash(message, key1, key2, iv)
    tdm_time = time.time() - start_time
    print(f"TDM Hash Zeit: {tdm_time:.6f} Sekunden")

    #start_time = time.time()
    #sha3_hash = SHA3_256.new()
    #sha3_hash.update(message)
    #end_time = time.time()
    #sha3_time = end_time - start_time
    #print(f"SHA Zeit: {sha3_time} Sekunden")
