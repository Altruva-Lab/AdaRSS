from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="distilbert-base-uncased",
    # timeout=300,           # seconds – 5 minutes
    # max_retries=5,
    local_dir="./distilbert-local"   # saves to a local folder
)
print("Download complete!")


# usage
# model = DistilBertForSequenceClassification.from_pretrained("./distilbert-local", num_labels=3)
# tokenizer = DistilBertTokenizer.from_pretrained("./distilbert-local")