# Python Fake

## 🌟 Overview

This project provides a `Fake` class that can be used to replace any object in a test, in development environment or in any other situation where you need to replace an object with a fake one.

The tries to provide a mock implementation for any usage, including properties, items, length, iterator, return value, await value, etc so that it never fails in runtime due to a missing implementation.

On the other hand, sometimes other pieces of code expect a certain implementation and the default implementation of the `Fake` class is not enough. In this case, you can use the `__Fake_...` parameters in the constructor to provide a more specific implementation.

At the moment, it doesn't provide tools for monitoring how the object was used, but it is planned to be implemented in the future.

### 🔎 Sample Usage

Fakeing the `picamera2` module of Raspberry Pi so that one can run the code on a non-Raspberry Pi development environment:

```python
from fake import Fake

sys.modules['picamera2'] = Fake(
    _Fake__props={
        'Picamera2': Fake(
            _Fake__return_value=Fake(
                _Fake__props={
                    'capture_array': Fake(
                        _Fake__return_value=np.zeros((1, 1, 3), dtype=np.uint8),
                    ),
                },
            ),
        ),
    },
)
```

## ⚙️ Parameters

A `Fake` object can be created with the following parameters:

- `_Fake__props`: A dictionary that contains the properties of the object and their respective values.
- `_Fake__items`: A dictionary that contains the items of the object and their respective values.
- `_Fake__list`: A list that contains the items of the object. (in case the index is a number and not listed in the `__items` dictionary). It also sets the length of the object if `_Fake__length` is not set.
- `_Fake__return_value`: The return value of the object when it is called.
- `_Fake__await_value`: The return value of the object when it is awaited.
- `_Fake__length`: The length of the object when it is queried via the `len` function.
- `_Fake__iter`: The iterator of the object when it is queried via the `iter` function.

## 📦 Installation

### Pip

```bash
pip install python-fake
```

### Poetry

```bash
poetry add python-fake
```
