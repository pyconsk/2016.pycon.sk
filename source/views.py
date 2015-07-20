from flask import Flask, request, send_from_directory, render_template

app = Flask(__name__, static_url_path='')

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title='Home')

@app.route('/code-of-conduct.html')
def code_of_conduct():
    return render_template('code-of-conduct.html', title='Home')

@app.route('/meetup-01.html')
def meetup_01():
    return render_template('meetup-01.html', title='Home')

@app.route('/meetup-02.html')
def meetup_02():
    return render_template('meetup-02.html', title='Home')

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
