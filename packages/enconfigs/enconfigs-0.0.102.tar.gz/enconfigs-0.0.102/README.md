```
  Author: Sujay RS
  Email: sujayy1983@gmail.com
```

# Encrypted configurations
Encrypt and decrypt a sensitive yaml or json configuration file with ease.

# Encrypt/Decrypt YAML or JSON configurations
This module encrypts sensitive yaml/json configurations and decrypts data
as needed by the application/script. It offers the following two modes to 
handle encryption/decryption keys.

# Modes - Managing symmetric keys

1. Default mode: Library generates encryption keys and maintains it for
   decryption/distribution.

2. User owns responsibility of managing his/her encrypted key in a secure vault 
   solution and feeds the key to ths library as required.

## Install this package
pip install enconfigs

## Tested on 

1. Ubuntu 22.04 with python 3.11
2. MacOS Sonoma 14.5 with python 3.11

Create sample scripts to test functionality

```
>>> from enconfigs.secureconfigs import SecureConfig
>>> inputdata={'key1': 'value1', 'key2': ['val2', 2]}  ## Input a json data
>>> secureobj = SecureConfig("/tmp/encryptedfile.yml") ## Target location of file where encrypted data must be stored.
True                                                   ## Indicates data was encrypted and stored successfully
>>> secureobj.update_encrypted_data(inputdata)         ## Directly provide config data that must be securely stored
>>> secureobj.decrypt_read_file()                      ## When application needs to read secure data then must call decrypt_read_file() method
{'key1': 'value1', 'key2': ['val2', 2]}

Note: Similar to the above string or list maybe an input for encryption 
```

## Future plan
- Easy key rotation and thus auto reencryption of data.
- Offer options to choose an asymmetric encryption algorithm.
- Test more complex data types.
- Test on more OS platforms.
- Test with more python versions.
- Actively support bugs.
