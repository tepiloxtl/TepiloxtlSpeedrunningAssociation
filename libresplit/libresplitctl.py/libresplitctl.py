#!/usr/bin/env python
import socket
import struct
import sys

SOCKET_PATH = "/run/user/1000/libresplit.sock"

def send_command(command_byte):
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(SOCKET_PATH)

        # 4 bytes for length (Big Endian), followed by the data
        # '>I' means: Big Endian (>), Unsigned Integer (I)
        payload = bytes([command_byte])
        length_header = struct.pack('>I', len(payload))

        sock.sendall(length_header + payload)
        print(f"Sent command: {command_byte} (Header: {length_header.hex()} | Payload: {payload.hex()})")
        sock.close()

    except FileNotFoundError:
        print(f"Error: Socket file not found at {SOCKET_PATH}")
    except ConnectionRefusedError:
        print("Error: The application is not running or refused the connection.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: libresplitctl.py <command or number>")
        print('"libresplitctl.py help" for list of commands')
        sys.exit(1)

    cmd = sys.argv[1]
    match cmd:
        case "startorsplit":
            send_command(0)
        case "stoporreset":
            send_command(1)
        case "cancel":
            send_command(2)
        case "unsplit":
            send_command(3)
        case "skipsplit":
            send_command(4)
        case "exit":
            send_command(5)
        case n if n.isdigit():
            send_command(int(cmd))
        case "help":
            print("""Available commands:
  startorsplit  - Start the timer/Split if timer is running
  stoporreset   - Stop the timer/Reset the timer if its stopped
  cancel        - Cancel the run
  unsplit       - Unsplit the timer
  skipsplit     - Skip the current split
  exit          - Closes LibreSplit
  help          - Show this help message""")
        case _:
            print("Usage: libresplitctl.py <command or number>")
            print('"libresplitctl.py help" for list of commands')
            sys.exit(1)

    # commands:
    # 0 = CTL_CMD_START_SPLIT, /*!< Start or split */
    # 1 = CTL_CMD_STOP_RESET, /*!< Stop or reset */
    # 2 = CTL_CMD_CANCEL, /*!< Cancel run */
    # 3 = CTL_CMD_UNSPLIT, /*!< Undo split */
    # 4 = CTL_CMD_SKIP, /*!< Skip split */
    # 5 = CTL_CMD_EXIT, /*!< Exit */
