import planetterp
import json
import time

def fetch_all_courses():
    all_courses = []
    offset = 0
    limit = 100

    while True:
        batch = planetterp.courses(limit=limit, offset=offset)
        if not batch:
            break
        all_courses.extend(batch)
        print(f"Fetched {len(batch)} at offset {offset}")
        offset += limit
        time.sleep(0.2)  # Be nice to the server

    return all_courses

def format_courses(courses):
    formatted = []
    for course in courses:
        dept = course['department'].upper()
        course_num = course['course_number']
        if dept and course_num:
            formatted.append(f"{dept}{course_num}")
    return formatted

# Usage
all_courses = fetch_all_courses()
formatted_courses = format_courses(all_courses)
with open("courses.json", "w") as f:
    json.dump(formatted_courses, f, indent=2)
