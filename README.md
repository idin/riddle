# *Riddle*

Riddle is a Python library for encryption.

# Installation

```bash
pip install riddle
```

# Usage

## ``Riddle``
```python
from riddle import Riddle
riddle = Riddle(key=1245)
encrypted = riddle.encrypt(obj=['Hello World!', 123])
print('Encrypted:\n\n', encrypted, '\n\n')
decrypted = riddle.decrypt(encrypted)
print('Decrypted:\n\n', decrypted)
```

**produces:** 
> Encrypted:
>
> wpLCr8OCfFjDjcKowqnDqcOFbcKYwrXDmcOXeMK6woZuwpVbw47DpMKiQ8OHwpnCr8Khw5XDpcKVw43Dm8Kdwr_Cq3N5wrrCokDCpsKJwpt1woXCmFjDmMOFwo7Cp8KIwoHCgcKNwprCocKhf8KKwpdobMKSwqTCpG_CosKGVMKWwpc= 
>
> Decrypted:
>
> ['Hello World!', 123]
>

## ``SecretKeeper``
```python
from riddle import SecretKeeper
from pandas import DataFrame

data = DataFrame({
    'name': ['John', 'Jack', 'Joe'], 
    'age': [12, 13, 14], 
    'random': [[1,2,3], [1,2,3], [1]]
})

data['age_divided_by_ten'] = data['age'] / 10

keeper = SecretKeeper()

anonymized_data = keeper.anonymize(data=data)

identified_data = keeper.identify(data=anonymized_data)

data.equals(identified_data) # returns True
```