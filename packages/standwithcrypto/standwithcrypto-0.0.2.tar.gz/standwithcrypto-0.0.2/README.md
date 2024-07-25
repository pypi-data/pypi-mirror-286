# Stand with Crypto (Unofficial)

Third-party API wrapper for [Stand with Crypto](https://www.standwithcrypto.org/). I am not affiliated with Stand with Crypto in any way.

## Prerequisites
Python 3.6+

## Source
https://github.com/samuel-poon/standwithcrypto

## Installation 
```bash
pip3 install standwithcrypto
```

## Quick Start
```python
import standwithcrypto

client = standwithcrypto.Client()

all_people = client.get_all_people()
print(all_people)
```

