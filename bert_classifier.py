import torch
import torch.nn as nn
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from read_datasets import read_data

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=1)

data_jasons = {"reddit": "example_reddit_data_set.json", "wikipedia": "wikipedia_data_set.json", "news": "wikipedia_data_set.json"}

is_train = True
load_model = False
load_optimizer = False

if load_model:
    model.load_state_dict(torch.load('bert_classifier.pth'))

def tokenize_data(texts, labels, max_length=128):
    input_ids = []
    attention_masks = []
    
    for text in texts:
        encoded = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=max_length,
            padding='max_length',
            return_attention_mask=True,
            truncation=True,
            return_tensors='pt'
        )
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])
    
    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)
    labels = torch.tensor(labels, dtype=torch.float)
    
    return input_ids, attention_masks, labels

def trainer(epochs_num, model, criterion, device, optimizer, train_dataloader,val_dataloader ):
    for epoch in tqdm(range(epochs_num)):
        model.train()
        train_accuracy = 0
        for batch in train_dataloader:
            batch = tuple(t.to(device) for t in batch)
            inputs = {'input_ids': batch[0],
                    'attention_mask': batch[1],
                    'labels': batch[2]}
            
            outputs = model(**inputs)
            logits = outputs.logits
            predictions = [1 if i > 0.5 else 0 for i in logits]
            N = len(predictions)
            for i in range(N):
                if predictions[i] == inputs['labels'][i]:
                    train_accuracy += 1
            loss = criterion(logits.view(-1), inputs['labels'].view(-1))
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        train_accuracy /= len(train_dataloader.dataset)
        # Validation
        model.eval()
        val_accuracy = 0
        for i, batch in enumerate(val_dataloader):
            batch = tuple(t.to(device) for t in batch)
            inputs = {'input_ids': batch[0],
                    'attention_mask': batch[1],
                    'labels': batch[2]}
            
            with torch.no_grad():
                outputs = model(**inputs)
            
            logits = outputs.logits
            predictions = [1 if i > 0.5 else 0 for i in logits]
            N = len(predictions)
            for i in range(N):
                if predictions[i] == inputs['labels'][i]:
                    val_accuracy += 1
        
        val_accuracy /= len(val_dataloader.dataset)
        print(f"Epoch {epoch+1}/{epochs_num} - Validation Accuracy: {val_accuracy:.4f}, Train Accuracy: {train_accuracy:.4f}")
        torch.save(model.state_dict(), 'bert_classifier.pth')
        torch.save(optimizer.state_dict(), 'optimizer.pth')
        torch.save({ epoch: i }, 'epoch.pth')

def evaluate(model, criterion, device, dataloader):
    model.eval()
    accuracy = 0
    predictions = []
    for i, batch in enumerate(dataloader):
        batch = tuple(t.to(device) for t in batch)
        inputs = {'input_ids': batch[0],
                'attention_mask': batch[1],
                'labels': batch[2]}
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        logits = outputs.logits
        batch_predictions = [1 if i > 0.5 else 0 for i in logits]
        predictions.extend(batch_predictions)
        
        N = len(batch_predictions)
        for i in range(N):
            if batch_predictions[i] == inputs['labels'][i]:
                accuracy += 1
    
    accuracy /= len(dataloader.dataset)
    print(f"Accuracy: {accuracy:.4f}")
    
    return predictions

data = read_data(data_jasons)
# for key in data_jasons.keys():
#     data_path = data_jasons[key]
#     with open(data_path, 'r') as file:
#         json_data = json.load(file)
#         if key == "reddit":
#             for item in json_data.values():
#                 data.append((item['human_comment'], 0))
#                 data.append((item['AI_comment'], 1))
#         else:
#             for item in json_data.values():
#                 data.append((item['human_comment'], 0))
#                 data.append((item['AI_comment'], 1))


print("data size:", len(data), "\n")
train_data, test_data = train_test_split(data, test_size=0.2)
train_texts = [] 
train_labels = []
val_texts = []
val_labels = []
for item in train_data:
    train_texts.append(item[0])
    train_labels.append(item[1])
for item in test_data:
    val_texts.append(item[0])
    val_labels.append(item[1])



train_inputs, train_masks, train_labels = tokenize_data(train_texts, train_labels) #TODO add the data
val_inputs, val_masks, val_labels = tokenize_data(val_texts, val_labels) # TODO add the data 

batch_size = 32

train_data = TensorDataset(train_inputs, train_masks, train_labels)
train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

val_data = TensorDataset(val_inputs, val_masks, val_labels)
val_dataloader = DataLoader(val_data, batch_size=batch_size, shuffle=False)

optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
epochs_num = 10
criterion = nn.BCEWithLogitsLoss()

if load_optimizer:
    optimizer.load_state_dict('optimizer.pth')
    epochs_num -= torch.load('epoch')
if is_train:
    trainer(epochs_num, model, criterion ,device, optimizer, train_dataloader, val_dataloader)
else:
    predctions, accuracy = evaluate(model, criterion, device, val_dataloader)

