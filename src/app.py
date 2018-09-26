import json
import math
import os

from flask import (Flask, url_for, render_template, redirect)

app = Flask(__name__)

def load_data():
    file_path = os.path.join(app.static_folder, 'data.json')
    with open(file_path, "r", encoding="utf8") as read_file:
        data = json.load(read_file)
    return data

@app.route('/')
def index():
    all_series = load_data()
    return render_template('index.html', all_series=all_series, ongoing=True)

@app.route('/completed')
def completed():
    all_series = load_data()
    return render_template('index.html', all_series=all_series, ongoing=False)

ELEMENTS_PER_PAGE = 12

class Paginator:
    def __init__(self, num_of_elements, current_page):
        self.num_of_elements = num_of_elements
        self.current_page = current_page

    def has_pages(self):
        return self.num_of_elements > ELEMENTS_PER_PAGE
        
    def on_first_page(self):
        return self.current_page == 1

    def has_more_pages(self):
        return self.current_page * ELEMENTS_PER_PAGE <= self.num_of_elements

    def last_page(self):
        return math.ceil(self.num_of_elements / ELEMENTS_PER_PAGE)

@app.route('/series/<string:abbr>', defaults={'page': 1})
@app.route('/series/<string:abbr>/<int:page>')
def series(abbr, page):
    all_series = load_data()
    
    for series in all_series:
        if series['abbr'] == abbr:
            images = os.listdir(os.path.join(app.static_folder, "img/" + abbr))

            total_volumes = len(images)

            # series that hasn't release any volume
            if total_volumes == 0:
                msg = 'Currently no volumes are available.'
                return render_template('series.html', series=series, msg=msg)

            start = (page - 1) * ELEMENTS_PER_PAGE
            end = page * ELEMENTS_PER_PAGE
            images = images[start:end]
            
            # no image due to page out of bounds
            if not images:
                return redirect(url_for('series', abbr=abbr))

            paginator = Paginator(total_volumes, page)
            
            return render_template('series.html', series=series, images=images, paginator=paginator)

    # unable to find the series
    msg = 'Unable to find the series.'
    return render_template('error.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)