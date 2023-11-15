# your_app/services/pinecone_service.py
from django.forms.models import model_to_dict
import pinecone
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import torch

def upsert_data_in_pinecone(model_instances, batch_size=64):
    # Assuming you have a function to convert your model data to vectors

    pinecone.init(
    api_key="e4c53b89-8118-4366-ab22-fa10e01496f1",
    environment="gcp-starter"  # find next to API key in console
    )
    index_name = "evsu-cc"

        # check if the abstractive-question-answering index exists
        
    index = pinecone.Index(index_name)
  
    if not isinstance(model_instances, list):
        # If a single instance is passed, convert it to a list
        model_instances = [model_instances]
    for i in tqdm(range(0, len(model_instances), batch_size)):
        # find end of batch
        i_end = min(i + batch_size, len(model_instances))
        # extract batch
        batch = model_instances[i:i_end]
        
        # generate embeddings for batch
        emb = [convert_to_vector(model_instance) for model_instance in batch]
        
        # get metadata
        meta = [model_to_dict(model_instance) for model_instance in batch]
        
        # create unique IDs
        ids = [str(model_instance.id) for model_instance in batch]
        
        # add all to upsert list
        to_upsert = list(zip(ids, emb, meta))
        
        # upsert/insert these records to pinecone
        _ = index.upsert(vectors=to_upsert)

def convert_to_vector(model_instance):
    # Assuming 'answer' is a field in your model
    answer = model_instance.answer
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    retriever = SentenceTransformer("flax-sentence-embeddings/all_datasets_v3_mpnet-base", device=device)
    
    # Use the global retriever to generate embeddings
    vector = retriever.encode(answer).tolist()
    
    return vector