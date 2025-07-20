from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, field_validator
import planetterp
import dotenv

dotenv.load_dotenv()

# Define structured output schema
class ProfSummary(BaseModel):
    courses: list[str]
    professor: str
    rating: float
    summary: str
    
    @field_validator('rating')
    def round_rating(cls, v):
        if v is None:
            return v
        return round(v, 2)

class CourseSummary(BaseModel):
    course: str
    professor: str
    rating: float
    gpa: float
    summary: str
    
    @field_validator('gpa')
    def round_gpa(cls, v):
        return round(v, 2)
    
    @field_validator('rating')
    def round_rating(cls, v):
        return round(v, 2)

def format_course_for_llm(course_data: dict) -> str:
    out = f"Course: {course_data['department']}{course_data['course_number']}\n"
    out += f"Average GPA: {course_data.get('average_gpa', 'N/A')}\n"
    out += f"Credits: {course_data.get('credits', 'N/A')}\n\n"
    out += f"Professors: {', '.join(course_data.get('professors', []))}\n\n"
    out += "Top Reviews:\n"
    for review in course_data.get('reviews', [])[::-1][:10]:
        out += f"- {review['review']}\n"
    return out

# Format professor data for LLM input
def format_professor_for_llm(prof_data: dict) -> str:
    out = f"Professor: {prof_data['name']}\n"
    out += f"Average Rating: {prof_data.get('average_rating', 'N/A')}\n"
    out += f"Courses: {', '.join(prof_data.get('courses', []))}\n\n"
    out += "Top Reviews:\n"
    for review in prof_data.get('reviews', [])[::-1][:10]:
        out += f"- {review['review']}\n"
    return out

# Set up the LLM using Groq
llm = ChatGroq(model="llama3-8b-8192")

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

# Fetch PlanetTerp professor data

def generate_summary(professor_name):
    prof_data = planetterp.professor(name=professor_name, reviews=True)
    if 'error' in prof_data:
        return None
    elif prof_data['average_rating'] is None and not prof_data.get('reviews'):
        return ProfSummary(
            courses=prof_data.get('courses', []),
            professor=prof_data['name'],
            rating=-1,
            summary="No reviews available."
        )
    formatted = format_professor_for_llm(prof_data)
    result = chain.invoke({"info_text": formatted})
    return result
