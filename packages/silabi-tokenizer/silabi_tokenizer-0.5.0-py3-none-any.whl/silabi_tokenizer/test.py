from hf_tokenizer import SilabiTokenizer

# Initialize the tokenizer
tokenizer = SilabiTokenizer()
# Encode a sample text
encoded_input = tokenizer("Hii ni mfano wa maandishi.")

# Decode the token ids back to text
decoded_text = tokenizer.decode(encoded_input['input_ids'])

print("Encoded Input:", encoded_input)
print("Decoded Text:", decoded_text)