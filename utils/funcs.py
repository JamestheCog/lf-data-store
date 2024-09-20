'''
Contains helper functions for manipulating data.
'''

from cryptography.fernet import Fernet

def encrypt(string, key):
    '''
    Given an rsa_init integer, encode a string "string" using RSA.
    '''
    fernet = Fernet(key.encode('utf-8'))
    return(fernet.encrypt(string.encode()).decode('utf-8'))

def decrypt(enc_string, key):
    '''
    Given an encoded string, decode it:
    '''
    fernet = Fernet(key.encode('utf-8'))
    return(fernet.decrypt(enc_string).decode('utf-8'))
    