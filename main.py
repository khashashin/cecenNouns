import json


def main():
    # open data.csv file
    with open('data.csv', 'r', encoding='utf-8') as f:
        # read the file
        data = f.read()
        # split the data into lines
        lines = data.splitlines()
        # print lines
        for line in lines:
            # continue if line contains ,
            if ',' in line:
                continue

            # continue if first character is uppercase
            if line[1].isupper() and line[1] != 'Ӏ':
                continue

            # remove first character if it "
            if line[0] == '"':
                line = line[1:]

            # remove last character if it "
            if line[-1] == '"':
                line = line[:-1]

            # write to json file
            write_to_json(line)
            print("Line written to json file: {}".format(line))


def write_to_json(line):
    with open('new_data.json', 'r+', encoding='utf-8') as f:
        _data = {}
        try:
            _data = json.load(f)
        except json.decoder.JSONDecodeError:
            f.write(json.dumps({}) + "\n")

        _data[line] = line

        f.seek(0)
        json.dump(_data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
