from transformers import BertTokenizer
import sys
sys.path.insert(0, '../Vocab')

from vocab import solidity_tokens

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
pre_len = len(tokenizer)

num_added_tokens = tokenizer.add_tokens(solidity_tokens)
print('Number of tokens added:', num_added_tokens)

# Print the vocabulary size before and after adding Solidity tokens
print('Vocabulary size before:', pre_len)
print('Vocabulary size after:', len(tokenizer))

tokenizer.save_pretrained('tokenizer-solidity')


