from src.data_loader import read_file
from src.preprocessor import LegalTextPreprocessor, setup_nltk
from transformers import LongformerTokenizer

def main(file_path: str):
    # Ensure NLTK resources are downloaded
    setup_nltk()

    # Load the document
    text = read_file(file_path)

    # Initialize the Longformer tokenizer
    tokenizer = LongformerTokenizer.from_pretrained('allenai/longformer-base-4096')

    # Create an instance of LegalTextPreprocessor
    preprocessor = LegalTextPreprocessor(tokenizer)

    # Preprocess the document
    original_text, segments, cleaned_text, tokens, structured_text, chunks = preprocessor.preprocess_doc(text)


if __name__ == "__main__":
    # Provide the path to a legal document file
    file_path = 'path_to_legal_document.txt'

    # Run the main function
    original_text, segments, cleaned_text, tokens, structured_text, chunks = main(file_path)

    # Print a summary of the processed data
    print("Original Text:", original_text[:10])
    print("\nSegments:", segments[:5])
    print("\nCleaned Text:", cleaned_text[:10])
    print("\nTokens:", tokens[:1])
    print("\nStructured Text:", structured_text[:10])
    print("\nChunks:", chunks[:1])
