import json
import matplotlib.pyplot as plt


    # Read the JSON file
with open('./model parameters/accuracies.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
# Create a figure and axis
train_accuracies = data['train_accuracies']
validation_accuracies = data['val_accuracies']
epochs = range(1, len(train_accuracies) + 1)
plt.plot(train_accuracies, label='Training Accuracy')
plt.plot(validation_accuracies, label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training and Validation Accuracy')
plt.savefig('./accuracy.png')
plt.show()
    