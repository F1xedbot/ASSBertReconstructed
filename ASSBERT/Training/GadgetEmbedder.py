import sys
sys.path.insert(0, '../Vocab')

import torch
from transformers import BertModel, BertTokenizer
from GadgetExtract import CodeExtractor

class CodeEmbedder:
    def __init__(self, model_name='bert-base-uncased', tokenizer_name='tokenizer-solidity'):
        # Load the tokenizer with Solidity tokens
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name)

        # Initialize the BERT model
        self.model = BertModel.from_pretrained(model_name, output_hidden_states=True)
        self.model.resize_token_embeddings(len(self.tokenizer))

    def generate_input_ids_and_attention_mask(self, code_gadgets, max_seq_length=512):
        # Initialize lists to store the padded encodings and attention masks
        padded_encodings = []
        attention_masks = []

        # Tokenize and encode each code gadget, and apply padding/truncation
        for gadget in code_gadgets:
            # Truncate long sequences if they exceed max_seq_length
            if len(gadget) > max_seq_length:
                gadget = gadget[:max_seq_length]

            encoding = self.tokenizer.encode(
                gadget, max_length=max_seq_length, padding='max_length', truncation=True)
            padded_encodings.append(encoding)

            # Create an attention mask
            attention_mask = [1] * len(encoding)
            while len(attention_mask) < max_seq_length:
                attention_mask.append(0)
            attention_masks.append(attention_mask)

        # Convert the padded encodings and attention masks to PyTorch tensors
        input_ids = torch.tensor(padded_encodings)
        attention_masks = torch.tensor(attention_masks)
        return input_ids, attention_masks

    def cls_embedding_and_mean_pooling(self, input_ids, attention_masks):
        # Pass the input_ids and attention_masks to the BERT model for processing
        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask=attention_masks)

        # Extract the last hidden state (embeddings)
        last_hidden_state = outputs.last_hidden_state

        # Stage 1: [CLS] Token Embedding
        cls_embedding = last_hidden_state[:, 0, :]

        # Stage 2: Mean Pooling
        mean_pooled = torch.mean(cls_embedding, dim=0)

        return mean_pooled

    def embed_code(self, code_gadgets, max_seq_length=512):
        input_ids, attention_masks = self.generate_input_ids_and_attention_mask(
            code_gadgets, max_seq_length)
        mean_pooled = self.cls_embedding_and_mean_pooling(input_ids, attention_masks)
        return mean_pooled

    def run(self, filename):
        extractor = CodeExtractor()
        code_gadgets = extractor.run(filename)
        embedding = self.embed_code(code_gadgets)
        return embedding

#Example usage:
# code_embedder = CodeEmbedder()
# filename = "../../DataPreprocessing/input.sol"
# embedding = code_embedder.run(filename)
# print(embedding)

