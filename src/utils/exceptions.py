class LuthorBaseException(Exception):
    """Base exception class for Luthor application."""
    pass

class DuplicateDocumentError(LuthorBaseException):
    """Raised when attempting to upload a document that already exists in the database."""

    def __init__(self, document_id):
        self.document_id = document_id
        super().__init__(f"Document with ID {document_id} already exists.")

class DatabaseConnectionError(LuthorBaseException):
    """Raised when there is an issue connecting to the database (Pinecone)."""
    pass

class InvalidQueryError(LuthorBaseException):
    """Raised when the user submits an invalid or empty query."""
    pass

class DocumentProcessingError(LuthorBaseException):
    """Raised when there is an error processing a document (e.g., during text extraction or chunking)."""
    pass

class EmbeddingGenerationError(LuthorBaseException):
    """Raised when there is an error generating embeddings (e.g., OpenAI API issues)."""
    pass

class AnswerGenerationError(LuthorBaseException):
    """Raised when there is an error generating an answer to a query."""
    pass

class ConfigurationError(LuthorBaseException):
    """Raised when there is a configuration issue (e.g., missing API keys)."""
    pass
