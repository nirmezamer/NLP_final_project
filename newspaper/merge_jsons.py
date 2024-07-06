import json
human_path_list = ["newspaper/bbc_articles.json", "newspaper/articles_edited_13_53.json"]
ai_path_list = ["newspaper/AI_articles.json"]
human_data = {}

for path in human_path_list:
    with open(path, 'r', encoding='utf-8') as file:
        human_data.update(json.load(file))

ai_data = {}

for path in ai_path_list:
    with open(path, 'r', encoding='utf-8') as file:
        ai_data.update(json.load(file))

data = {}
data["human"] = []
data["AI"] = []
for key in human_data.keys():
    data["human"].append(human_data[key])
for key in ai_data.keys():
    data["AI"].append(ai_data[key])

with open("newspaper/newspapers_data.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

