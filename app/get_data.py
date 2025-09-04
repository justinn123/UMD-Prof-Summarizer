from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, field_validator
from flask import current_app as app
from app import cache
import planetterp
import dotenv

dotenv.load_dotenv()

# Define structured output schema
class ProfSummary(BaseModel):
    # courses: list[str]
    professor: str
    slug: str
    rating: float
    summary: str
    
    @field_validator('rating')
    def round_rating(cls, v):
        if v is None:
            return v
        return round(v, 2)

# Set up the LLM using Groq
llm = ChatGroq(model="llama-3.3-70b-versatile")

# Define the output parser
parser = PydanticOutputParser(pydantic_object=ProfSummary)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", 
"""
You are an assistant that summarizes university course or professor reviews.

Your task is to synthesize key patterns from student feedback, focusing on:
- Teaching style
- Difficulty
- Engagement
- Clarity
- Recurring praise or complaints

Do not quote or paraphrase individual reviews. Instead, analyze the overall sentiment and highlight common themes.

You must conclude with a clear recommendation: based on the reviews, should students take this professor/course, or consider alternatives?

⚠️ Your response MUST be a valid JSON object that strictly follows this Pydantic schema:
{format_instructions}

⚠️ Do NOT include any extra text, explanation, markdown formatting, or commentary — return ONLY the raw JSON.
"""
),
    ("human", "{info_text}")
]).partial(format_instructions=parser.get_format_instructions())

# Combine into a chain
chain = prompt | llm | parser

# Fetch PlanetTerp professor data and return output
def generate_summary(professor_name):
    cache_key = f"summary:{professor_name}"
    
    cached = get_from_cache(cache_key)
    
    if cached:
        return cached
    
    prof_data = use_api(professor_name)
    if not prof_data:
        return None
    
    result = get_results(prof_data)
    set_to_cache(cache_key, result)
    
    return result

# Helper Functions
# Get summary of professor
def get_results(prof_data: dict) -> str:
    if not prof_data['average_rating']:
        return ProfSummary(
            professor=prof_data['name'],
            slug = prof_data['slug'],
            rating=-1,
            summary="Nobody has reviewed this professor yet."
        )
    out = f"Professor: {prof_data['name']}\n"
    out += f"Slug: {prof_data['slug']}\n"
    out += f"Average Rating: {prof_data.get('average_rating', 'N/A')}\n"
    out += "Top Reviews:\n"
    for review in prof_data.get('reviews', [])[::-1][:10]:
        out += f"- {review['review']}\n"
    result = chain.invoke({"info_text": out})
    return result

def get_from_cache(key):
    try:
        cached = cache.get(key)
        if cached:
            app.logger.info("Using cached data")
            return cached
    except Exception as e:
        app.logger.error(f"Error on get: {e}")
    return None

def set_to_cache(key, value):
    try:
        cache.set(key, value)
    except Exception as e:
        app.logger.error(f"Error on set: {e}")
        
def use_api(professor_name):
    app.logger.info("Calling API directly")
    data = planetterp.professor(name=professor_name, reviews=True)
    return None if 'error' in data else data
