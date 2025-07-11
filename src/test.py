from requests_html import HTMLSession

www = HTMLSession()

def get_terms():
    url = 'https://app.testudo.umd.edu/soc/'
    r = www.get(url)
    terms = []
    for e in r.html.find('#term-id-input option'):
        terms.append(e.attrs['value'])
    return terms


print(get_terms())