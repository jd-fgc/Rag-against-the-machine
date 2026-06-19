from pydantic import BaseModel, Field
from typing import List
import uuid


class MinimalSource(BaseModel):
    """Minimal source reference with file path and character positions."""
    file_path: str
    first_character_index: int
    last_character_index: int


class Chunk(MinimalSource):
    """An indexed chunk from the knowledge base with text content."""
    text: str
    chunk_type: str


class UnansweredQuestion(BaseModel):
    """A question without an answer or retrieved sources."""
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    """A question with its expected sources and ground truth answer."""
    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    """A dataset of RAG questions, answered or unanswered."""
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    """Search results for a single question."""
    question_id: str
    question_str: str
    retrieved_sources: List[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    """Search results with a generated answer."""
    answer: str


class StudentSearchResults(BaseModel):
    """Full search results output for a dataset."""
    search_results: List[MinimalSearchResults | MinimalAnswer]
    k: int


class StudentSearchResultsAndAnswer(StudentSearchResults):
    """Full search results with generated answers for a dataset."""
    search_results: List[MinimalAnswer | MinimalSearchResults]
