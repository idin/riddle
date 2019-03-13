# Riddle

Riddle is a Python library for encryption.

## Installation

```bash
pip install riddle
```

## Usage

```python
from riddle import Riddler

# initialize a Riddler
r = Riddler(key=1234)

# encrypt an object
encrypted = r.encrypt(x=['Hello World!', 123])

print(encrypted)
# acKiw6jCnlvCvsKqw5_CoMOCw6dSwp_DpMK5w5jCmMKNYsOnwos_wrZ7emrCnMKEw4p6

# decrypt the encrypted object
decrypted = r.decrypt(x=encrypted)
print(decrypted)
# ['Hello World!', 123]
```