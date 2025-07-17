from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
import planetterp
import dotenv

dotenv.load_dotenv()  # Make sure GROQ_API_KEY is set in your .env

# Define structured output schema
class Response(BaseModel):
    courses: list[str]
    professor: str
    summary: str

def format_course_for_llm(course_data: dict) -> str:
    out = f"Course: {course_data['course']}\n"
    out += f"Department: {course_data.get('department', 'N/A')}\n"
    out += f"Average Rating: {course_data.get('average_rating', 'N/A')}\n"
    out += f"Difficulty: {course_data.get('average_gpa', 'N/A')}\n"
    out += f"Credits: {course_data.get('credits', 'N/A')}\n\n"
    out += "Top Reviews:\n"

# Format professor data for LLM input
def format_professor_for_llm(prof_data: dict) -> str:
    out = f"Professor: {prof_data['name']}\n"
    out += f"Department: {prof_data.get('department', 'N/A')}\n"
    out += f"Average Rating: {prof_data.get('average_rating', 'N/A')}\n"
    out += f"Courses: {', '.join(prof_data.get('courses', []))}\n\n"
    out += "Top Reviews:\n"
    for review in prof_data.get('reviews', [])[:5]:
        out += f"- {review['review']}\n"
    return out

# Set up the LLM using Groq
llm = ChatGroq(model="llama3-8b-8192")

# Define the output parser
parser = PydanticOutputParser(pydantic_object=Response)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a helpful assistant that summarizes professor/course reviews.\n"
     "You must respond with ONLY a valid JSON object, following this Pydantic format:\n{format_instructions}"),
    ("human", "{info_text}")
]).partial(format_instructions=parser.get_format_instructions())

# Combine into a chain
chain = prompt | llm | parser

# Fetch PlanetTerp professor data
prof_data = planetterp.professor(name="Justin Wyss-Gallifent", reviews=True)
course_data = planetterp.course(name="CMSC454", reviews=True)
formatted = format_professor_for_llm(prof_data)

# Run the chain
result = chain.invoke({"info_text": formatted})

# Print the structured output
print(result)
