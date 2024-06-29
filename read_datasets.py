import json

def read_data(data_key_path):
    data = []
    for key in data_key_path.keys():
        data_path = data_key_path[key]
        with open(data_path, 'r') as file:
            json_data = json.load(file)
            if key == "reddit":
                for item in json_data.values():
                    data.append((item['human_comment'], 0))
                    data.append((item['AI_comment'], 1))
            else:
                for item in json_data.values():
                    data.append((item['data'], item['ai_generated']))
    return data