from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration, AutoTokenizer

model = RagTokenForGeneration.from_pretrained_question_encoder_generator("facebook/dpr-question_encoder-single-nq-base", "facebook/bart-large")

question_encoder_tokenizer = AutoTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
generator_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large")

tokenizer = RagTokenizer(question_encoder_tokenizer, generator_tokenizer)
model.config.use_dummy_dataset = True
model.config.index_name = "exact"
retriever = RagRetriever(model.config, question_encoder_tokenizer, generator_tokenizer)

model.save_pretrained("./")
tokenizer.save_pretrained("./")
retriever.save_pretrained("./")