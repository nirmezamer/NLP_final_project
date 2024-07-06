import json

def read_data(data_key_path):
    data = []
    for key in data_key_path.keys():
        data_path = data_key_path[key]
        if key == "reddit":
            with open(data_path, 'r') as file:
                json_data = json.load(file)
                for item in json_data.values():
                    data.append((item['human_comment'], 0))
                    data.append((item['AI_comment'], 1))
        elif key == "wikipedia":
            with open(data_path, 'r') as file:
                json_data = json.load(file)
                for item in json_data.values():
                    data.append((item['Summary'], item['Is AI generated']))
        else:
            with open(data_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                for key in json_data.keys():
                    if key == "human":
                        for item in json_data[key]:
                            data.append((item, 0))
                    else:
                        for item in json_data[key]:
                            data.append((item, 1))
    return data