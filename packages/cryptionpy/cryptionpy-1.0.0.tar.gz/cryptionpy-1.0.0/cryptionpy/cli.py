import sys
from .encryption import encrypt_file_wrapper, decrypt_file_wrapper

def main():
    if len(sys.argv) < 4:
        print("Usage: cryptionpy <input_file> <output_file> <method> [--decrypt]")
        print("Method: 'base64' or 'emoji'")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    method = sys.argv[3]
    decrypt = '--decrypt' in sys.argv

    if decrypt:
        if decrypt_file_wrapper(input_file, output_file, method):
            print(f"Success: '{output_file}' has been created.")
        else:
            print(f"Error: Failed to create '{output_file}'.")
    else:
        if encrypt_file_wrapper(input_file, output_file, method):
            print(f"Success: '{output_file}' has been created.")
        else:
            print(f"Error: Failed to create '{output_file}'.")

if __name__ == '__main__':
    main()
