import pandas as pd
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# ✅ Load dataset
books = pd.read_csv("my_dataset.csv", engine="python", quotechar='"', escapechar='\\')

# ✅ Extract and save descriptions as a text file
books["tagged_description"].to_csv("tagged_description.txt", sep="\n", index=False, header=False)

# ✅ Load and preprocess documents
raw_documents = TextLoader("tagged_description.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20, separator="\n")
documents = text_splitter.split_documents(raw_documents)

# ✅ Initialize embedding model & ChromaDB
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db_books = Chroma.from_documents(documents, embedding=embedding_model)

# ✅ Retrieve manga recommendations
def retrieve_semantic_recommendations(query: str, top_k: int = 10) -> pd.DataFrame:
    recs = db_books.similarity_search(query, k=top_k)
    books_list = [recs[i].page_content.strip('"').split()[0] for i in range(len(recs))]
    return books[books["isbn13"].astype(str).isin(books_list)]

# ✅ Terminal-based input loop
if __name__ == "__main__":
    print("\n🎌 Welcome to the Manga Recommendation System 🎌")
    
    while True:
        query = input("\n🔍 Enter a manga description (or type 'exit' to quit): ")
        
        if query.lower() == "exit":
            print("👋 Goodbye!")
            break
        
        recommendations = retrieve_semantic_recommendations(query, top_k=5)
        
        if recommendations.empty:
            print("⚠️ No similar manga found.")
        else:
            print("\n📚 Recommended Manga:")
            print(recommendations[["title", "isbn13"]].to_string(index=False))

