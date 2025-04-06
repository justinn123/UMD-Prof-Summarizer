from requests_html import HTMLSession

www = HTMLSession()

def get_terms(active_only=True):
    url = 'https://app.testudo.umd.edu/soc/'
    r = www.get(url)
    terms = []
    for e in r.html.find('#term-id-input option'):
        terms.append(e.attrs['value'])
    return terms

def get_course(term, course):
    url = f'https://app.testudo.umd.edu/soc/search?course={course}&term={term}'
    r = www.get(url)
    return r.html.find('.course-list')[0].text

print(get_terms())