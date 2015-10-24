from flask import Flask, g, request, send_from_directory, render_template, abort
from flask.ext.babel import Babel, gettext

app = Flask(__name__, static_url_path='/static')
app.config['BABEL_DEFAULT_LOCALE'] = 'sk'
babel = Babel(app)


@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        g.current_lang = request.view_args['lang_code']
        if request.view_args['lang_code'] not in ('en', 'sk', 'de'):
            return abort(404)
        request.view_args.pop('lang_code')


@babel.localeselector
def get_locale():
    # try to guess the language from the user accept
    # header the browser transmits. The best match wins.
    # return request.accept_languages.best_match(['de', 'sk', 'en'])
    return g.get('current_lang', app.config['BABEL_DEFAULT_LOCALE'])


def _get_template_variables():
    variables = {
        'title': gettext('PyCon SK'),
        'logo': 'images/pycon_sk_logo_notext.svg'
    }

    if 'current_lang' in g:
        variables['lang_code'] = g.current_lang
    else:
        variables['lang_code'] = app.config['BABEL_DEFAULT_LOCALE']

    return variables


@app.route('/<lang_code>/index.html')
def index():
    return render_template('index.html', **_get_template_variables())


@app.route('/<lang_code>/speaking.html')
def speaking():
    return render_template('speaking.html', **_get_template_variables())


@app.route('/<lang_code>/sponsoring.html')
def sponsoring():
    return render_template('sponsoring.html', **_get_template_variables())


@app.route('/<lang_code>/tickets.html')
def tickets():
    return render_template('tickets.html', **_get_template_variables())


@app.route('/<lang_code>/code-of-conduct.html')
def code_of_conduct():
    return render_template('code-of-conduct.html', **_get_template_variables())


@app.route('/<lang_code>/spy.html')
def spy():
    variables = _get_template_variables()
    variables['title'] = gettext('SPy o. z.')

    return render_template('spy.html', **variables)


@app.route('/<lang_code>/thank-you.html')
def thank_you():
    return render_template('thank-you.html', **_get_template_variables())


@app.route('/<lang_code>/meetup.html')
def meetup():
    return render_template('meetup.html', **_get_template_variables())


@app.route('/<lang_code>/ba-01-meetup.html')
def ba_meetup_01():
    variables = _get_template_variables()
    variables['logo'] = 'images/bratislava_logo.svg'

    return render_template('ba-01-meetup.html', **variables)


@app.route('/<lang_code>/ba-02-meetup.html')
def ba_meetup_02():
    variables = _get_template_variables()
    variables['logo'] = 'images/bratislava_logo.svg'

    return render_template('ba-02-meetup.html', **variables)


@app.route('/<lang_code>/ba-03-meetup.html')
def ba_meetup_03():
    variables = _get_template_variables()
    variables['logo'] = 'images/bratislava_logo.svg'

    return render_template('ba-03-meetup.html', **variables)


@app.route('/<lang_code>/ba-04-meetup.html')
def ba_meetup_04():
    variables = _get_template_variables()
    variables['logo'] = 'images/bratislava_logo.svg'

    return render_template('ba-04-meetup.html', **variables)


@app.route('/<lang_code>/ba-05-meetup.html')
def ba_meetup_05():
    variables = _get_template_variables()
    variables['logo'] = 'images/bratislava_logo.svg'

    return render_template('ba-05-meetup.html', **variables)


if __name__ == "__main__":
    app.run(debug=True)
