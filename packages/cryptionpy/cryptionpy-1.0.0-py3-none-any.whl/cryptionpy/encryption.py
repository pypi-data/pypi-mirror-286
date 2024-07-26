import base64
import os
from pprint import pformat

MAX_STR_LEN = 70
OFFSET = 10

alphabet = [
    "\U0001f600",
    "\U0001f603",
    "\U0001f604",
    "\U0001f601",
    "\U0001f605",
    "\U0001f923",
    "\U0001f602",
    "\U0001f609",
    "\U0001f60A",
    "\U0001f61b",
]

def obfuscate(VARIABLE_NAME, file_content):
    b64_content = base64.b64encode(file_content.encode()).decode()
    index = 0
    code = f'{VARIABLE_NAME} = ""\n'
    for _ in range(int(len(b64_content) / OFFSET) + 1):
        _str = ''
        for char in b64_content[index:index + OFFSET]:
            byte = str(hex(ord(char)))[2:]
            if len(byte) < 2:
                byte = '0' + byte
            _str += '\\x' + str(byte)
        code += f'{VARIABLE_NAME} += "{_str}"\n'
        index += OFFSET
    code += f'exec(__import__("\\x62\\x61\\x73\\x65\\x36\\x34").b64decode({VARIABLE_NAME}.encode("\\x75\\x74\\x66\\x2d\\x38")).decode("\\x75\\x74\\x66\\x2d\\x38"))'
    return code

def deobfuscate(VARIABLE_NAME, obfuscated_content):
    exec_globals = {}
    exec(obfuscated_content, exec_globals)
    return base64.b64decode(exec_globals[VARIABLE_NAME]).decode()

def chunk_string(in_s, n):
    return "\n".join(
        "{}\\".format(in_s[i: i + n]) for i in range(0, len(in_s), n)
    ).rstrip("\\")

def encode_string(in_s, alphabet):
    d1 = dict(enumerate(alphabet))
    d2 = {v: k for k, v in d1.items()}
    return (
        'exec("".join(map(chr,[int("".join(str({}[i]) for i in x.split())) for x in\n'
        '"{}"\n.split("  ")])))\n'.format(
            pformat(d2),
            chunk_string(
                "  ".join(" ".join(d1[int(i)] for i in str(ord(c))) for c in in_s),
                MAX_STR_LEN,
            ),
        )
    )

def decode_string(encoded_content, alphabet):
    d1 = dict(enumerate(alphabet))
    d2 = {v: k for k, v in d1.items()}
    exec_globals = {}
    exec(encoded_content, exec_globals)
    decoded_content = "".join(chr(int("".join(str(d2[i]) for i in x.split()))) for x in exec_globals[""].split("  "))
    return decoded_content

def encrypt_file(input_file, output_file, method):
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"File '{input_file}' not found.")

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as in_f:
        file_content = in_f.read()

    if method == 'base64':
        VARIABLE_NAME = "encrypted_code"
        encrypted_content = obfuscate(VARIABLE_NAME, file_content)
    elif method == 'emoji':
        encrypted_content = encode_string(file_content, alphabet)
    else:
        raise ValueError("Method must be 'base64' or 'emoji'.")

    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write(encrypted_content)

    return output_file

def decrypt_file(input_file, output_file, method):
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"File '{input_file}' not found.")

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as in_f:
        encrypted_content = in_f.read()

    if method == 'base64':
        VARIABLE_NAME = "encrypted_code"
        decrypted_content = deobfuscate(VARIABLE_NAME, encrypted_content)
    elif method == 'emoji':
        decrypted_content = decode_string(encrypted_content, alphabet)
    else:
        raise ValueError("Method must be 'base64' or 'emoji'.")

    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write(decrypted_content)

    return output_file

def encrypt_file_wrapper(input_file, output_file, method):
    try:
        encrypt_file(input_file, output_file, method)
        return True
    except Exception as e:
        return False

def decrypt_file_wrapper(input_file, output_file, method):
    try:
        decrypt_file(input_file, output_file, method)
        return True
    except Exception as e:
        return False
