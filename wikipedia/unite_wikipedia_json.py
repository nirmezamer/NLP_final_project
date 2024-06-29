import json
import random

# Step 1: Load the JSON data from the files
with open('wikipedia/ai_wikipedia_summaries.json', 'r') as file:
    ai_data = json.load(file)
with open('wikipedia/human_wikipedia_summaries.json', 'r') as file:
    human_data = json.load(file)

# Step 2: Equalize the number of AI and human summaries
if len(ai_data) > len(human_data):
    ai_data = dict(random.sample(sorted(ai_data.items()), len(human_data)))
else:
    human_data = dict(random.sample(sorted(human_data.items()), len(ai_data)))

# Step 3: Add the 'Is AI generated' key to the data
ai_data = {key: {'Summary': value, 'Is AI generated': 1} for key, value in ai_data.items()}
human_data = {key: {'Summary': value, 'Is AI generated': 0} for key, value in human_data.items()}

# Step 4: Combine the AI and human data
combined_data = {**ai_data, **human_data}

# Step 5: Write the combined data to a new file
with open('wikipedia/wikipedia_summaries.json', 'w') as file:
    json.dump(combined_data, file, indent=4)

print(f"Combined data written to 'wikipedia/wikipedia_summaries.json'")
print(f"Total number of summaries : {len(combined_data)}")
print(f"Number of AI summaries    : {len(ai_data)}")
print(f"Number of human summaries : {len(human_data)}")
