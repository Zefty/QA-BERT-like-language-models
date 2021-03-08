# Test pytorch working 
import torch
x = torch.rand(5, 3)
print(x)

# Test Hugginface working 
from transformers import pipeline

# Open and read the article
question = "What is the capital of the Netherlands?"

# The 'r' means raw string so ignores escape codes e.g. ignores /n 
context = r"The four largest cities in the Netherlands are Amsterdam, Rotterdam, The Hague and Utrecht.[17] Amsterdam is the country's most populous city and nominal capital,[18] while The Hague holds the seat of the States General, Cabinet and Supreme Court.[19] The Port of Rotterdam is the busiest seaport in Europe, and the busiest in any country outside East Asia and Southeast Asia, behind only China and Singapore."

# Generating an answer to the question in context
qa = pipeline("question-answering")
answer = qa(question=question, context=context)

# Print the answer
print(f"Question: {question}")
print(f"Answer: '{answer['answer']}' with score {answer['score']}")

# Test RAG working 
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration

tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)
model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

input_dict = tokenizer.prepare_seq2seq_batch("who holds the record in 100m freestyle", return_tensors="pt") 

generated = model.generate(input_ids=input_dict["input_ids"]) 
print(tokenizer.batch_decode(generated, skip_special_tokens=True)[0])