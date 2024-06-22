import torch
import torch.nn as nn
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
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
    labels = torch.tensor(labels)
    
    return input_ids, attention_masks, labels

def trainer(epochs_num, model, device, loss, optimizer):
    for epoch in tqdm(range(epochs_num)):
        model.train()
        for batch in train_dataloader:
            batch = tuple(t.to(device) for t in batch)
            inputs = {'input_ids': batch[0],
                    'attention_mask': batch[1],
                    'labels': batch[2]}
            
            outputs = model(**inputs)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        
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
            predictions = torch.argmax(logits, dim=1)
            val_accuracy += (predictions == inputs['labels']).sum().item()
        
        val_accuracy /= len(val_dataloader.dataset)
        print(f"Epoch {epoch+1}/{epochs_num} - Validation Accuracy: {val_accuracy:.4f}")
        torch.save(model.state_dict(), 'bert_classifier.pth')
        torch.save(optimizer.state_dict(), 'optimizer.pth')
        torch.save({ epoch: i }, 'epoch.pth')
train_inputs, train_masks, train_labels = tokenize_data(train_texts, train_labels) #TODO add the data
val_inputs, val_masks, val_labels = tokenize_data(val_texts, val_labels) # TODO add the data 

batch_size = 32

train_data = TensorDataset(train_inputs, train_masks, train_labels)
train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

val_data = TensorDataset(val_inputs, val_masks, val_labels)
val_dataloader = DataLoader(val_data, batch_size=batch_size, shuffle=False)

optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
epochs_num = 5
if load_optimizer:
    optimizer.load_state_dict('optimizer.pth')
    epochs_num -= torch.load('epoch')


