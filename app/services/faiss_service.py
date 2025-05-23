import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

class FAQIndexer:
    def __init__(self):
        self.index = faiss.IndexFlatL2(384)  # 384 is the dimension of the embeddings
        self.faqs = []

    def index_faqs(self, faqs):
        """Index the FAQ data."""
        self.faqs = faqs
        questions = [faq['Question'] for faq in faqs]
        embeddings = model.encode(questions)
        self.index.add(np.array(embeddings))

    def retrieve_faqs(self, query, top_k=3):
        """Retrieve the most relevant FAQs based on the query."""
        if not self.faqs:
            raise ValueError("No FAQs have been indexed.")
        
        query_embedding = model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding), top_k)
        
        # Filter out invalid indices
        valid_indices = [i for i in indices[0] if i < len(self.faqs)]
        
        if not valid_indices:
            raise ValueError("No relevant FAQs found for the given query.")
        
        return [self.faqs[i] for i in valid_indices]

faq_indexer = FAQIndexer()
