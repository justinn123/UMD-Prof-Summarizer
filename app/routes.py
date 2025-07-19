from flask import redirect, request, session, url_for, render_template, current_app as app
from .scrapeTestData import generate_summary

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = None
    professor_name = None
    if request.method == 'POST':
        # Handle form submission
        professor_name = request.form.get('professor')
        course_name = request.form.get('course')
        if professor_name:
            summary = generate_summary(professor_name)
        
    return render_template('index.html', summary=summary, professor=professor_name)