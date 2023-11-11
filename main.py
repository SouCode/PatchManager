import json
from models.software import Software


def load_software_list():
    with open('config/software_list.json', 'r') as file:
        software_data = json.load(file)
        return [Software(**software) for software in software_data]


def main():
    software_list = load_software_list()
    for software in software_list:
        print(software)


if __name__ == "__main__":
    main()
