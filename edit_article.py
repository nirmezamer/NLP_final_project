import json

def delete_articles_json_mor():
        # Iterate over the keys in the JSON object
    to_delet_keys = []
    for key in data.keys():
        if len(data[key].split()) < 100:
            to_delet_keys.append(key)
            

    for key in to_delet_keys:
        del data[key]
    # Write the modified JSON back to the file
    with open("articles_edited.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



def delete_articles_json():
    # Iterate over the keys in the JSON object
    to_delet_keys = []
    for key in data.keys():
        # Filter out elements with less than 100 words
        data[key] = [string for string in data[key] if len(string.split()) >= 100]
        if len(data[key]) == 0:
            to_delet_keys.append(key)
        else:
            data[key] = data[key][0]


    for key in to_delet_keys:
        del data[key]
    # Write the modified JSON back to the file
    with open("articles_edited_13_53.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
# Read the JSON file

with open('articles_13_53.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

delete_articles_json()
