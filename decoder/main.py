import yaml

class DTCDecoder():

    def __init__(self):
        self.data = {}

    def decode(self, data):
        category = self.decode_category(data)
        number = self.decode_number(data)

        return category + number

    def decode_category(self, data):
        letters = ["P", "C", "B", "N"]

        major = (data[0] >> 4) // 4
        minor = (data[0] >> 4) % 4

        return letters[major] + str(minor)

    def decode_number(self, data):
        digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

        lowest = digits[data[1] & 0b00001111]
        lower = digits[data[1] >> 4]
        high = digits[data[0] & 0b00001111]

        return high + lower + lowest

class DTCDatabase():

    def __init__(self):
        self.data = {}

    def load(self, path):
        n = 0
        with open(path, "r") as file:
            for entry in yaml.safe_load(file):
                self.data[entry["code"].lower()] = entry
                n += 1
        return n

    def query(self, code):
        if code.lower() in self.data:
            return self.data[code.lower()]
        return None



database = DTCDatabase()
decoder = DTCDecoder()

# Load database
n = database.load("../data/data.yaml")
print(f'[info] loaded {n} DTC data entries')

# Shell
while True:
    command = input("> ").split(" ")

    if command[0] == "exit":
        break

    if command[0] == "help":
        print("dtc read          - read trouble codes")
        print("dtc clear         - clear trouble codes")
        print("dtc decode [code] - decode hex-encoded trouble code")
        print("dtc query [dtc]   - query dtc information in database")

    if command[0] == "dtc":

        if command[1] == "read":
            print("[error] Error occured while trying to read dtc")

        if command[1] == "clear":
            print("[error] Error occured while trying to clear dtc")

        if command[1] == "decode":
            data = int(command[2], 16)
            low = data & 0b11111111
            high = data >> 8

            code = decoder.decode([high, low])
            print(f'{code} (0x{data:04X})')

        if command[1] == "query":
            result = database.query(command[2])

            if result == None:
                data = int(command[2], 16)
                low = data & 0b11111111
                high = data >> 8
                result = database.query(decoder.decode([high, low]))

            if result == None:
                print("[error] No database entry found for this dtc")
            else:
                print(f'Code: {result["code"]}')
                print(f'Description: {result["description"]}')

