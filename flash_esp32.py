import esptool
import sys

def flash_bin(port, baudrate, bin_file):
    # Initialize the esptool with the given port and baudrate
    esptool_args = [
        '--port', port,
        '--baud', baudrate,
        'write_flash', '0x1000', bin_file
    ]
    
    # Call the esptool main function with the provided arguments
    esptool.main(esptool_args)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python flash_esp32.py <port> <baudrate> <bin_file>")
        sys.exit(1)

    port = sys.argv[1]
    baudrate = sys.argv[2]
    bin_file = sys.argv[3]

    flash_bin(port, baudrate, bin_file)
