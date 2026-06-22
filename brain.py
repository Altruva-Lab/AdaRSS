import pandas as pd
import torch
import joblib
import re
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sentence_transformers import SentenceTransformer, util
import numpy as np
import os

# Suppress warnings for cleaner output
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ------------------- 1. LOAD DATA -------------------
df = pd.read_csv('data/sample_annotated.csv')
texts = (df['job_title'] + ": " + df['skill']).tolist()
labels = df['label'].tolist()

print("🚀 AdaRSS DistilBERT + Sentence‑Transformer Personalization")
print(f"Loaded {len(texts)} samples.")
print(f"Label distribution:\n{pd.Series(labels).value_counts().sort_index()}")

# ------------------- 2. TOKENIZATION & TRAIN/VAL SPLIT -------------------
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
encodings = tokenizer(texts, truncation=True, padding=True, max_length=64)

class SkillDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    def __len__(self):
        return len(self.labels)

X_train, X_val, y_train, y_val = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)
train_enc = tokenizer(X_train, truncation=True, padding=True, max_length=64)
val_enc = tokenizer(X_val, truncation=True, padding=True, max_length=64)
train_dataset = SkillDataset(train_enc, y_train)
val_dataset = SkillDataset(val_enc, y_val)

print(f"Train: {len(train_dataset)}, Val: {len(val_dataset)}")

# ------------------- 3. CLASS WEIGHTS (for imbalanced data) -------------------
class_counts = pd.Series(labels).value_counts().sort_index()
total = len(labels)
# Use inverse frequency weighting
class_weights = {i: total / (len(class_counts) * count) for i, count in class_counts.items()}
print(f"Class weights: {class_weights}")

# ------------------- 4. MODEL -------------------
model = DistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased',
    num_labels=3
)

# ------------------- 5. TRAINING ARGUMENTS (updated for v5.x) -------------------
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=8,                      # More epochs for larger dataset
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    logging_steps=10,
    eval_strategy='epoch',                   # renamed from evaluation_strategy
    save_strategy='epoch',
    load_best_model_at_end=True,
    metric_for_best_model='accuracy',
    weight_decay=0.01,
    # logging_dir is deprecated – remove it
)

# ------------------- 6. METRICS -------------------
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    acc = accuracy_score(labels, preds)
    cm = confusion_matrix(labels, preds)
    print("Confusion Matrix:\n", cm)
    print("\nClassification Report:\n", classification_report(labels, preds, target_names=['Enduring','Emergent','Transient']))
    return {'accuracy': acc}

# ------------------- 7. TRAINER (without tokenizer argument) -------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
    # tokenizer=tokenizer,   # REMOVED – not accepted in newer versions
)

# ------------------- 8. TRAIN & SAVE -------------------
trainer.train()
model.save_pretrained('./api/model/adarss-distilbert')
tokenizer.save_pretrained('./api/model/adarss-distilbert')
print("💾 Model and tokenizer saved to ./api/model/adarss-distilbert")

# ------------------- 9. LOAD SENTENCE-TRANSFORMER FOR SIMILARITY -------------------
similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Sentence-Transformer loaded.")

# ------------------- 10. INFERENCE HELPER (for classification) -------------------
def classify_skill_text(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=64)
    outputs = model(**inputs)
    pred = outputs.logits.argmax().item()
    mapping = {0: "Enduring", 1: "Emergent", 2: "Transient"}
    return pred, mapping[pred]

# ------------------- 11. PERSONALIZATION ENGINE (using embeddings) -------------------
class PersonalizationEngine:
    def __init__(self, history_text):
        self.history = history_text
        self.history_embedding = similarity_model.encode(history_text, convert_to_tensor=True)

    def compute_similarity(self, target_skill):
        target_embedding = similarity_model.encode(target_skill, convert_to_tensor=True)
        sim = util.pytorch_cos_sim(self.history_embedding, target_embedding).item()
        return sim

    def generate_advice(self, target_skill):
        sim = self.compute_similarity(target_skill)
        _, durability = classify_skill_text(f"Generic Worker: {target_skill}")

        if sim >= 0.35:
            advice_type = "Continuous Upscaling"
            desc = "✅ Your background aligns well. You have relevant experience."
            roadmap = f"Advanced path: Deepen {target_skill} expertise through certifications and applied projects. Since {target_skill} is {durability}, it's a solid investment."
        elif sim >= 0.15:
            advice_type = "Career Broadening"
            desc = f"🌉 Your skills transfer to {target_skill}, though not directly. You can leverage your existing knowledge."
            roadmap = f"Consider a bridging course or project that connects your current expertise to {target_skill}. {target_skill} is {durability}."
        else:
            advice_type = "Change of Profession"
            desc = f"⚠️ {target_skill} represents a significant pivot from your current path."
            roadmap = f"Plan for 18-36 months of dedicated learning. Start with fundamentals, build portfolio, then pursue internships or entry-level roles. Note: {target_skill} is currently {durability}."

        return {
            "type": advice_type,
            "description": desc,
            "roadmap": roadmap,
            "durability": durability,
            "similarity": sim
        }

# ------------------- 12. DEMO -------------------
print("\n" + "="*70)
print("🧑‍💼 ADA RSS PERSONALIZED CAREER ADVICE ENGINE (DEMO)")
print("="*70)

personas = [
    ("Aisha (Backend Dev)", "5 years Python, Django, REST APIs, SQL databases, AWS", "Kubernetes"),
    ("James (Registered Nurse)", "10 years ER Nurse, Epic Systems, patient triage, clinical workflows", "Health Informatics"),
    ("Maria (Accountant)", "8 years Financial Audit, QuickBooks, GAAP compliance, Excel modeling", "UI/UX Design"),
    ("David (DevOps)", "4 years Linux admin, Bash scripting, AWS, Terraform, CI/CD", "MLOps")
]

for name, history, target in personas:
    print(f"\n--- 👤 {name} ---")
    engine = PersonalizationEngine(history)
    advice = engine.generate_advice(target)
    print(f"History: {history}")
    print(f"Target: {target}")
    print(f"🏷️ Classification: {advice['durability']}")
    print(f"📌 Advice Type: {advice['type']}")
    print(f"💬 {advice['description']}")
    print(f"🗺️ {advice['roadmap']}")
    print(f"📊 Similarity Score: {advice['similarity']:.3f}")

print("\n" + "="*70)
print("✨ Done. Model and tokenizer saved.")
print("="*70)