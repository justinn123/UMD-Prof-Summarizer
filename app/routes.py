import json
from flask import jsonify, redirect, request, session, url_for, render_template, current_app as app
from .get_data import generate_summary

@app.route('/', methods=['GET', 'POST'])
def home():
    summary = None
    professor_name = None
    if request.method == 'POST':
        # Handle form submission
        professor_name = request.form.get('professor')
        if not professor_name:
            return render_template('index.html', error="Please enter a professor's name.")
        try:
            summary = generate_summary(professor_name)
            if not summary:
                return render_template('index.html', error="Professor not found or no reviews available.")
        except Exception as e:
            app.logger.error(f"Error: {e}")
            return render_template('error.html', error="There was an error getting professor data. Please try again later.")
    return render_template('index.html', summary=summary)

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '').lower()
    matches = []

    try:
        with open('app/static/professors.json') as f:
            professors = json.load(f)
        app.logger.info("Successfully loaded professor list\n")
    except Exception as e:
        app.logger.error(f"There was an error: {e}")
        return []

    for prof in professors:
        if query in prof.lower():
            matches.append(prof)

    return jsonify(matches[:5])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/Error')
def error():
    return render_template('error.html', error="There was an error")

@app.route('/InProgress')
def progress():
    return render_template('error.html', error="This page is still in progress. Please check back later.")
