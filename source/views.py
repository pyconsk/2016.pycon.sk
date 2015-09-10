from flask import Flask, request, send_from_directory, render_template

app = Flask(__name__, static_url_path='')

@app.route('/')
@app.route('/index.html')
def index():
    variables = {
        'title': 'PyCon SK',
        'logo': 'python_logo_notext.svg'
            }
    return render_template('index.html', **variables)

@app.route('/code-of-conduct.html')
def code_of_conduct():
    variables = {
        'title': 'PyCon SK',
        'logo': 'python_logo_notext.svg'
            }
    return render_template('code-of-conduct.html', **variables)

@app.route('/spy.html')
def spy():
    variables = {
        'title': 'SPy o. z.',
        'logo': 'python_logo_notext.svg'
            }
    return render_template('spy.html', **variables)

@app.route('/thank-you.html')
def thank_you():
    variables = {
        'title': 'PyCon SK',
        'logo': 'python_logo_notext.svg'
            }
    return render_template('thank-you.html', **variables)


@app.route('/meetup.html')
def meetup():
    variables = {
        'title': 'PyCon SK',
        'logo': 'python_logo_notext.svg'
            }
    return render_template('meetup.html', **variables)

@app.route('/01-meetup.html')
@app.route('/ba-01-meetup.html')
def ba_meetup_01():
    variables = {
        'title': 'PyCon SK',
        'logo': 'bratislava_logo.svg'
            }
    return render_template('ba-01-meetup.html', **variables)

@app.route('/02-meetup.html')
@app.route('/ba-02-meetup.html')
def ba_meetup_02():
    variables = {
        'title': 'PyCon SK',
        'logo': 'bratislava_logo.svg'
            }
    return render_template('ba-02-meetup.html', **variables)

@app.route('/ba-03-meetup.html')
def ba_meetup_03():
    variables = {
        'title': 'PyCon SK',
        'logo': 'bratislava_logo.svg'
            }
    return render_template('ba-03-meetup.html', **variables)

@app.route('/ba-04-meetup.html')
def ba_meetup_04():
    variables = {
        'title': 'PyCon SK',
        'logo': 'bratislava_logo.svg'
            }
    return render_template('ba-04-meetup.html', **variables)


# Serve static files via flask so curl can collect them to build static pages

@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/static/images/<path:path>')
def send_images(path):
    return send_from_directory('/static/images', path)

@app.route('/static/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('/static/fonts', path)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('/static', path)


if __name__ == "__main__":
    app.run(debug=True)
