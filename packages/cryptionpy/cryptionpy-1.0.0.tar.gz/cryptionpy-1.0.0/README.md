# cryptionpy 1.0.0

`cryptionpy` is a Python package designed for easy encryption and decryption of Python files using either base64 or emoji obfuscation methods. With `cryptionpy`, you can secure your source code or obfuscate it for various purposes.

## Benefits

- **Easy to Use**: Simple command-line interface and Python module functionality.
- **Two Encryption Methods**: Choose between base64 or emoji obfuscation for your needs.
- **Flexible**: Works as both a command-line tool and a Python module.
- **Efficient**: Quickly encrypt and decrypt files with minimal setup.

## Installation

You can install the package using pip:

```bash
pip install cryptionpy
```

## Usage

### As a Command-Line Tool

#### Encryption

```bash
cryptionpy <input_file> <output_file> <method>
```

- method
    * emoji
    * base64

#### Decryption

```bash
cryptionpy <input_file> <output_file> base64 --decrypt
```

- `<input_file>`: The Python file you want to encrypt or decrypt.
- `<output_file>`: The file where the encrypted or decrypted code will be saved.
- `<method>`: The encryption method, either `base64` or `emoji`.
- `--decrypt`: Optional flag to decrypt the file instead of encrypting.

### As a Module

#### Encryption

```python
from cryptionpy import encrypt_file

if encrypt_file('input_file.py', 'output_file.py', 'base64'):
    print("Encrypted")
else:
    print("Not Encrypted")
```

#### Decryption

```python
from cryptionpy import decrypt_file

if decrypt_file('input_file.py', 'output_file.py', 'base64'):
    print("Decrypted")
else:
    print("Not Decrypted")
```

## Examples

### Command-Line

For Base64 encryption:

```bash
cryptionpy input_file.py output_file.py base64
```

For Base64 decryption:

```bash
cryptionpy input_file.py output_file.py base64 --decrypt
```

For Emoji encryption:

```bash
cryptionpy input_file.py output_file.py emoji
```

### As a Module

#### Encryption

```python
from cryptionpy import encrypt_file

if encrypt_file('input_file.py', 'output_file.py', 'base64'):
    print("Encrypted")
else:
    print("Not Encrypted")
```

#### Decryption

```python
from cryptionpy import decrypt_file

if decrypt_file('input_file.py', 'output_file.py', 'base64'):
    print("Decrypted")
else:
    print("Not Decrypted")
```

## Benefits

- **Enhanced Security**: Protect your source code from unauthorized access or tampering.
- **Versatility**: Use either base64 or emoji obfuscation based on your needs.
- **Ease of Use**: Integrate easily into your workflow, whether via CLI or programmatically.

## Thanks

Thank you for using `cryptionpy`. Your feedback and contributions are greatly appreciated! If you encounter any issues or have suggestions for improvements, please let us know.
