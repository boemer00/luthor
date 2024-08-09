import re
import nltk
from typing import List, Tuple
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from transformers import LongformerTokenizer

# Ensure nltk resources are downloaded during setup or first run
def setup_nltk():
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)

class LegalTextPreprocessor:
    def __init__(self, tokenizer, chunk_size=4096, overlap=0):
        """
        Initialize the LegalTextPreprocessor with a tokenizer and configuration for chunking.

        Args:
            tokenizer (object): The tokenizer object to encode and decode text.
            chunk_size (int): The desired size of each chunk.
            overlap (int): The number of tokens to overlap between chunks.
        """
        self.tokenizer = tokenizer
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def text_segmentation(self, text: str) -> List[str]:
        """
        Split text into smaller, manageable chunks with consideration for legal memo structures.

        Args:
            text (str): The full text to be segmented.

        Returns:
            List[str]: A list of segmented text chunks.
        """
        # Identify section breaks (e.g. double newlines, headings, and bullet points).
        pattern = r'(?<=\n)(?=\n)|(?<=\n)(?=\s*[\d-]+\s)|(?<=\n)(?=Section \d+|Article \d+)|(?<=\n)(?=\s*-\s)|(?<=\n)(?=\s*\*\s)'

        # Split the text using the defined pattern
        segments = re.split(pattern, text.strip())

        # Clean up the segments to remove any leading/trailing whitespace
        segmented_text = [segment.strip() for segment in segments if segment.strip()]

        return segmented_text

    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize the text into words, considering legal-specific tokens and preprocessing.

        Args:
            text (str): The text to be tokenized.

        Returns:
            List[str]: A list of tokens (words).
        """
        # Tokenize words using NLTK
        tokens = word_tokenize(text)

        # Convert to lowercase
        tokens = [token.lower() for token in tokens]

        # Remove stopwords specific to legal context
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]

        # Reduce tokens to their base form
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

        return tokens

    def clean_special_characters(self, text: str) -> str:
        """
        Clean up non-informative special characters or artifacts.

        Args:
            text (str): The text from which to remove special characters.

        Returns:
            str: Cleaned text with unnecessary special characters removed.
        """
        # Remove characters not usually found in legal texts
        cleaned_text = re.sub(r'[^\w\s,.!?;:()-]', '', text)

        return cleaned_text

    def preserve_structure(self, text: str) -> str:
        """
        Maintain the document's structural elements, such as headings.

        Args:
            text (str): The text to process for structural preservation.

        Returns:
            str: Text with preserved structure for headings and sections.
        """
        # Keep lines starting with capital words as headings
        structured_text = re.sub(r'(?m)^(?=[A-Z])(.+)$', r'## \1', text)

        return structured_text

    def create_chunks(self, text: str) -> List[str]:
        """
        Creates chunks of text for preprocessing, ensuring each chunk is within the specified size.

        Args:
            text (str): The full text to be chunked.

        Returns:
            List[str]: A list of text chunks.
        """
        # Tokenize the text using the tokenizer associated with this instance
        tokens = self.tokenizer.encode(text, add_special_tokens=True, truncation=True, max_length=self.chunk_size)

        # Split tokens into chunks of the specified size, considering overlap
        chunks = [tokens[i:i + self.chunk_size] for i in range(0, len(tokens), self.chunk_size - self.overlap)]

        # Decode each chunk back into text
        text_chunks = [self.tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]

        return text_chunks

    def preprocess_doc(self, text: str) -> Tuple[str, List[str], str, List[str], str, List[str]]:
        """
        Preprocess a legal document by executing a series of text processing steps, including chunking.

        Args:
            text (str): The full text of the legal document.

        Returns:
            Tuple: A tuple containing:
                - Original text (str)
                - Segmented text chunks (List[str])
                - Cleaned text (str)
                - Tokenized words (List[str])
                - Structured text (str)
                - Chunks (List[str])
        """
        # Step 1: Segmentation
        segments = self.text_segmentation(text)

        # Step 2: Clean special characters from the full text
        cleaned_text = self.clean_special_characters(text)

        # Step 3: Tokenize the cleaned text
        tokens = self.tokenize_text(cleaned_text)

        # Step 4: Preserve structure in the cleaned text
        structured_text = self.preserve_structure(cleaned_text)

        # Step 5: Create chunks from the structured text
        chunks = self.create_chunks(structured_text)

        return text, segments, cleaned_text, tokens, structured_text, chunks
