from flask import redirect, request, session, url_for, render_template, current_app as app
from .scrapeTestData import generate_summary

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = None
    professor_name = None
    if request.method == 'POST':
        # Handle form submission
        professor_name = request.form.get('professor')
        if professor_name:
            summary = generate_summary(professor_name)
        if not summary:
            return render_template('index.html', error="Professor not found or no reviews available.")
    return render_template('index.html', summary=summary)