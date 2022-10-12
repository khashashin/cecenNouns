import json


def sort_dict_by_query():
    query = 'та'
    # open new_data.json file as python dictionary
    with open('new_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # sort dictionary by key that ends with query
    sorted_data = sorted(data.items(), key=lambda x: x[0].endswith(query))
    # sorted_data = sorted(data.items(), key=lambda x: query in x[0])

    # write sorted dictionary to new file
    with open('sorted_data.json', 'w', encoding='utf-8') as f:
        json.dump(dict(sorted_data), f, ensure_ascii=False, indent=2)


def main():
    sort_dict_by_query()


if __name__ == "__main__":
    main()
