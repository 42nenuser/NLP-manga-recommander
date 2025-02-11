from langchain_community.embeddings import HuggingFaceEmbeddings

# ✅ Load Hugging Face model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ Sample text to encode
text = "Testing Hugging Face embeddings inside Docker."

# ✅ Generate embeddings
embedding_vector = embedding_model.embed_query(text)

# ✅ Print first 10 values for verification
print("\n✅ Embedding generated successfully!")
print("First 10 values:", embedding_vector[:10])

