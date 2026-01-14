from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
import dotenv
import os
dotenv.load_dotenv()

# Define the structure you want
class MovieReview(BaseModel):
    title: str = Field(description="Movie title")
    rating: int = Field(description="Rating out of 10")
    pros: List[str] = Field(description="List of positive points")
    cons: List[str] = Field(description="List of negative points")
    summary: str = Field(description="One line summary")

# Create parser
parser = PydanticOutputParser(pydantic_object=MovieReview)

# Prompt includes format instructions
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a movie critic. Analyze the given movie."),
    ("user", "Review the movie: {movie}\n\n{format_instructions}")
])

model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

chain = prompt | model | parser

# Run it
review = chain.invoke({
    "movie": "Inception",
    "format_instructions": parser.get_format_instructions()
})

# review is now a Python object!
# print(f"Title: {review.title}")
# print(f"Rating: {review.rating}/10")
# print(f"Pros: {review.pros}")
# print(f"Cons: {review.cons}")
# print(f"Summary: {review.summary}")

print(parser.get_format_instructions())