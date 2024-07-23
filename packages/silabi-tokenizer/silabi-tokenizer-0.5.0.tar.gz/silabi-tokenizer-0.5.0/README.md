# Swahili Syllabic Tokenizer
This repository hosts a custom tokenizer for Swahili text, designed to tokenize text into syllables using a syllabic vocabulary. The tokenizer is compatible with the Hugging Face transformers library, making it easy to integrate into NLP pipelines and models.

## Features
- Syllabic Tokenization: Tokenizes Swahili text into syllables based on a predefined syllabic vocabulary.
- Byte Fallback: Handles UTF-8 byte fallback for out-of-vocabulary tokens.
- Customizable: Easily extendable and adaptable for specific NLP tasks.

## Usage
### Installation
```
pip install -r requirements.txt
```
### Example
```
from hf_tokenizer import SilabiTokenizer

# Initialize the tokenizer
tokenizer = SilabiTokenizer()
# Encode a sample text
encoded_input = tokenizer("Hii ni mfano wa maandishi.")

# Decode the token ids back to text
decoded_text = tokenizer.decode(encoded_input['input_ids'])

print("Encoded Input:", encoded_input)
print("Decoded Text:", decoded_text)

```

### Contributions
Contributions and suggestions are welcome! Feel free to open an issue or submit a pull request.
