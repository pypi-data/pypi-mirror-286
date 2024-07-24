from pydantic import BaseModel, Field, SerializeAsAny
from typing import Literal, Optional, Union, Annotated

class Document(BaseModel):
    """Represents a document used as a ground truth when generating tests."""

    url: Optional[str] = None
    filepath: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None

class QuestionWithReason(BaseModel):
    question: str = Field(description="The question text.")
    reference_answer: str = Field(description="The expected response.")
    reason: str = Field(description="Used for explaining the reasoning behind the question.")

class SimpleQuestionGeneratorArgs(BaseModel):
    question_type: Literal["SimpleQuestion"] = "SimpleQuestion" # Type discriminator used for deserialization. Do not change.
    question_limit: int = Field(description="The number of questions to generate")
    temperature: float | None = Field(description="The temperature to use when generating questions", default=None)
    positive_examples: list[QuestionWithReason] = Field(description="A list of few-shot examples of good questions to help guide the question generation")
    negative_examples: list[QuestionWithReason] = Field(description="A list of few-shot examples of poorly phrased or incorrect questions to help guide the question generation", default=[])
    extra_criteria: list[str] = Field(description="A list of extra criteria to evaluate the quality of the generated questions.", default=[])

class HallucinationInducingQuestionGeneratorArgs(BaseModel):
    question_type: Literal["HallucinationInducing"] = "HallucinationInducing" # Type xdiscriminator used for deserialization. Do not change.
    question_limit: int = Field(description="The number of questions to generate")
    temperature: float | None = Field(description="The temperature to use when generating questions", default=None)
    positive_examples: list[QuestionWithReason] = Field(description="A list of few-shot examples of good questions to help guide the question generation")
    negative_examples: list[QuestionWithReason] = Field(description="A list of few-shot examples of poorly phrased or incorrect questions to help guide the question generation", default=[])
    extra_criteria: list[str] = Field(description="A list of extra criteria to evaluate the quality of the generated questions.", default=[])

# This is a discriminated union. What we want is to have a list of question generator configs, and to be able to send that list from the client/cli to the server and have it correctly deserialize.
# Breaking it down:
#  - Union means the type GeneratorArgs can refer to EITHER SimpleQuestionGeneratorArgs or HallucinationInducingQuestionGeneratorArgs
#  - When deserializing one of these GeneratorArgs over the wire, look at the question_type field to determine which of the two we're currently deserializing. It's a constant with a different value for the two classes (SimpleQuestion or HallucinationInducing)
#  - The SerializeAsAny is just there to suppress some warnings caused by a bug in pydantic.
GeneratorArgs = SerializeAsAny[Annotated[Union[SimpleQuestionGeneratorArgs, HallucinationInducingQuestionGeneratorArgs], Field(discriminator="question_type")]]

class QuestionGenerationConfig(BaseModel):
    # TODO: Remove source_documents and replace with knowledge_bases when that code is all ready.
    source_docs: list[Document] = Field(description="List of documents to use as the ground truth when generating questions.")
    name: str = Field(description="Friendly name for the configuration used in logging, error reporting and the UI.")
    knowledge_bases: list[str] = Field(description="List of knowledge bases to use for generating questions. Uses knowledge base UUIDs.")
    question_configs: list[GeneratorArgs] = Field(description="List of question generator configurations.")
