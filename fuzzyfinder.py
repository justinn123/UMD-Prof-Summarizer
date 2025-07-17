from rapidfuzz import process, fuzz
import json

# Load prebuilt lists
with open("professors.json", "r") as f:
    professors = json.load(f)

with open("courses.json", "r") as f:
    courses = json.load(f)

def extract_entities(user_input, prof_threshold=80, course_threshold=80):
    words = user_input.lower().replace(",", "").split()

    # 1. Try fuzzy match against chunks of 1–4 consecutive words
    potential_matches = [" ".join(words[i:j]) for i in range(len(words)) for j in range(i+1, min(i+4, len(words))+1)]

    best_prof, prof_score = None, 0
    best_course, course_score = None, 0

    for chunk in potential_matches:
        prof, p_score, _ = process.extractOne(chunk, professors, scorer=fuzz.token_sort_ratio)
        course, c_score, _ = process.extractOne(chunk.upper().replace(" ", ""), courses, scorer=fuzz.token_sort_ratio)

        if p_score > prof_score:
            best_prof, prof_score = prof, p_score
        if c_score > course_score:
            best_course, course_score = course, c_score

    return {
        "professor": best_prof if prof_score >= prof_threshold else None,
        "course": best_course if course_score >= course_threshold else None,
        "prof_score": prof_score,
        "course_score": course_score
    }

query = "summarize anwar mamat for cmsc 330"
result = extract_entities(query)

print(result)
# Output:
# {
#   'professor': 'Kristjana Maddux',
#   'course': 'COMM107',
#   'prof_score': 94,
#   'course_score': 98
# }
