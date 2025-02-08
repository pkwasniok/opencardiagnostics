import argparse
import elm327

ELM327_ADDRESS = "10:21:3E:47:A6:45"

parser = argparse.ArgumentParser(prog="OBD Scanner")

parser.add_argument("--command", action="store", type=str, help="execute command")
parser.add_argument("--reset", action="store_true", help="soft reset adapter")
parser.add_argument("--read-version", action="store_true", help="read adapter version")
parser.add_argument("--read-voltage", action="store_true", help="read battery voltage")
parser.add_argument("--calibrate-voltage", action="store", type=float, help="calibrate battery voltage reading")
parser.add_argument("--read-dtc", action="store_true", help="read dtc")
parser.add_argument("--read-pending-dtc", action="store_true", help="read pending dtc")
parser.add_argument("--clear", action="store_true", help="clear dtc and stored values")
parser.add_argument("--monitor", action="store_true", help="monitor can bus")

args = parser.parse_args()

adapter = elm327.Adapter(ELM327_ADDRESS)

adapter.connect()

if args.command:
    adapter.write(args.command)
    response = adapter.read()
    print(response)

elif args.reset:
    print("Resetting adapter... ", end="")
    adapter.reset()
    print("OK")

elif args.read_version:
    print("Reading adapter version... ", end="")
    version = adapter.read_version()
    print("OK")

    print("Model: ELM327")
    print(f'Version: {version[1:]}')

elif args.calibrate_voltage:
    print("Calibrating battery voltage reading... ", end="")
    adapter.calibrate_voltage(args.calibrate_voltage)
    print("OK")

elif args.read_voltage:
    print("Reading battery voltage... ", end="")
    voltage = adapter.read_voltage()
    print("OK")

    print(f'Battery voltage: {voltage/100:4.2f} V')

elif args.read_dtc:
    print("Reading stored trouble codes... ", end="")
    adapter.read_dtc()
    print("OK")

elif args.read_pending_dtc:
    print("Reading pending trouble codes... ", end="")
    adapter.read_pending_dtc()
    print("OK")

elif args.clear:
    print("Clearing trouble codes and stored values... ", end="")
    adapter.clear()
    print("OK")

elif args.monitor:
    print("Starting monitoring CAN bus...")
    adapter.write("AT MA")

    while True:
        frame = adapter.read()
        print(frame)

else:
    while True:
        command = input("> ")
        if command == "exit":
            break
        adapter.write(command)
        response = adapter.read()
        print(response)

adapter.disconnect()

