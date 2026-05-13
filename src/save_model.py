# save_models.py — much simpler now
from sentence_transformers import CrossEncoder
import os

os.makedirs("./models/reranker", exist_ok=True)

print("Saving reranker...")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
reranker.save("./models/reranker")
print("Done.")