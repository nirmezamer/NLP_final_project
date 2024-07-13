import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure and axes
fig, ax = plt.subplots(figsize=(14, 8))

# Define rectangle positions with more space between them
rects = {
    "Human Data Collection": (0, 0.6),
    "AI Data Generation": (0.25, 0.6),
    "Data Preperation": (0.5, 0.6),
    "Model Training": (0.75, 0.6),
}

# Add rectangles and labels with adjusted size and color
for key, (x, y) in rects.items():
    ax.add_patch(patches.Rectangle((x, y), 0.22, 0.15, edgecolor='black', facecolor='white'))
    plt.text(x + 0.115, y + 0.075, key, ha='center', va='center', fontsize=12)

# Add arrows
arrow_props = dict(facecolor='black', arrowstyle='->')
for i in range(len(rects) - 1):
    start = list(rects.values())[i]
    end = list(rects.values())[i + 1]
    ax.annotate('', xy=(start[0] + 0.075, start[1] + 0.22), xytext=(end[0], end[1] + 0.075), arrowprops=arrow_props)

# Add detailed texts with max 3 lines
texts = [
    "Collect texts from\nWikipedia, Reddit,\nand newspapers",
    "Generate AI-written\ntexts mimicking human\nwriting using Gemini",
    "Clean, tokenize, and\nsplit data into\ntraining and test sets",
    "Train the model on\nlabeled human and\nAI-generated data"
]

# Adjust text positions to avoid overlap
text_positions = {
    "Data Collection": (0, 0.4),
    "AI Data Generation": (0.25, 0.4),
    "Data Preperation": (0.5, 0.4),
    "Model Training": (0.75, 0.4),
}

for (key, (x, y)), (tx, ty) in zip(rects.items(), text_positions.values()):
    plt.text(tx, ty, texts[list(rects.keys()).index(key)], ha='center', va='center', fontsize=10, wrap=True)

# Hide axes
ax.axis('off')

# Save and display the figure
plt.show()
