from flask import Flask, request, url_for, redirect, render_template, jsonify
import requests


app = Flask(__name__)

search_suggestions = []
results = []

def fetch_agencies():
    url = 'https://www.ecfr.gov/api/admin/v1/agencies.json'
    response = requests.get(url)

    # Ensure that the response is JSON and return the data
    if response.status_code == 200:
        return response.json()  # Parse JSON response
    else:
        print(f"Error fetching data: {response.status_code}")
        return []
    
agencies_data = fetch_agencies()
@app.route('/')
def hello():
    category = request.args.get('category')
    dynamic_inputs = generate_dynamic_inputs(category)
    for x in agencies_data.values():
        for i in x:
            search_suggestions.append(i.get('name'))
    return render_template('index.html', dynamic_inputs=dynamic_inputs)


@app.route('/search')
def search():
    query = request.args.get('q')
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    category = request.args.get('category')
    dynamic_inputs = generate_dynamic_inputs(category)
    if request.method == 'GET':
        # Check if the reset button was pressed
        if 'reset' in request.args:
            results.clear()
        else:
            if query or q1 and q2:
                if category == 'word_count':
                    results.append(f"The {query} has a word count of " + str(find_agency_word_count(query)))
                elif category == 'historical':
                    results.append(f"There were " + str(query_historical(q1, q2)) + " historical changes between the dates " + str(q1) + " and " + str(q2))
                elif category == 'corrections':
                    results.append(f"There have been " + str(query_corrections(query)) + " corrections on title number " + str(query))
    
    return render_template('index.html', query=query, results=results, category=category, dynamic_inputs=dynamic_inputs)

@app.route('/search_suggestions')
def search_suggestions_route():
    return jsonify(search_suggestions)
    
def Get_Size(response):
    """
    Fetch the full CFR content for a given title from the eCFR API.
    Returns the word count of the content.
    """
    for x in response.values():
        for i in x:
            return i.get('size')
    
# Calculates the word count for the given federal agency
def find_agency_word_count(name):
    word_count = 0
    # Ensure we are handling the correct data structure (list of agencies)
    for agency in agencies_data.values():
        for x in agency:
            if x.get('name') == name:
                for reference in x.get('cfr_references', []):
                    title = reference['title']
                    url = f'https://www.ecfr.gov/api/versioner/v1/ancestry/2025-04-08/title-{title}.json'  # Using today's date
                    response = requests.get(url)
                    return Get_Size(response.json())

    return word_count

def compare_ecfr_dates(first_date, second_date):
    url = f'https://www.ecfr.gov/api/search/v1/count?last_modified_after={first_date}&last_modified_before={second_date}'
    response = requests.get(url)
    for x in response.json().values():
        return x.get("total_count")
    
def query_corrections(title):
    count = 0
    url = f'https://www.ecfr.gov/api/admin/v1/corrections/title/{title}.json'
    response = requests.get(url)
    if response:
        for x in response.json().values():
            for i in x:
                count += 1
    return count

def query_historical(startDate, endDate):
    count = 0
    url = f'https://www.ecfr.gov/api/search/v1/results?last_modified_after={startDate}&last_modified_before={endDate}&order=relevance&paginate_by=results'
    response = requests.get(url)
    for x in response.json().values():
        for i in x:
            count += 1
    return count

def generate_dynamic_inputs(category):
    # Generate dynamic inputs based on category
    if category == 'word_count':
        return create_input('q', 'Enter agency name')
    elif category == 'historical':
        return (
            create_input('q1', 'On or after YYYY-MM-DD') +
            create_input('q2', 'On or before YYYY-MM-DD')
        )
    elif category == 'corrections':
        return create_input('q', 'Title number')
    else:  # default for "All"
        return create_input('q', 'Enter agency name')

def create_input(name, placeholder):
    return f'''
        <input type="text" name="{name}" placeholder="{placeholder}" value="{placeholder}" list="searchSuggestions" />
        <datalist id="searchSuggestions"></datalist>
    '''