from flask import Flask, g, request, send_from_directory, render_template, abort, make_response
from flask.ext.babel import Babel, gettext

app = Flask(__name__, static_url_path='/static')
app.config['BABEL_DEFAULT_LOCALE'] = 'sk'
app.jinja_options = {'extensions': ['jinja2.ext.with_']}
babel = Babel(app)

LOGO_PYCON = 'images/pycon_sk_logo_notext.png'
LOGO_MEETUP_BA = 'images/bratislava_logo.png'
LANGS = ('en', 'sk')
SITEMAP = {
    'sitemap.xml': {'prio': '0.9', 'freq': 'weekly', 'lastmod': '2015-10-26T22:05:00+00:00'},
    'index.html': {'prio': '1', 'freq': 'weekly', 'lastmod': '2015-10-26T22:05:00+00:00'},
    'sponsoring.html': {'prio': '0.9', 'freq': 'weekly', 'lastmod': '2015-10-26T22:05:00+00:00'},
    'speaking.html': {'prio': '0.9', 'freq': 'weekly', 'lastmod': '2015-10-26T22:05:00+00:00'},
    'tickets.html': {'prio': '1', 'freq': 'weekly', 'lastmod': '2015-10-26T22:00:05+00:00'},
    'spy.html': {'prio': '0.75', 'freq': 'monthly', 'lastmod': '2015-09-10T20:00:00+00:00'},
    'code-of-conduct.html': {'prio': '0.75', 'freq': 'monthly', 'lastmod': '2015-09-10T20:00:00+00:00'},
    'meetup.html': {'prio': '0.66', 'freq': 'weekly', 'lastmod': '2015-10-26T22:56:48+00:00'},
    'ba-01-meetup.html': {'prio': '0.5', 'freq': 'monthly', 'lastmod': '2015-06-29T20:06:00+00:00'},
    'ba-02-meetup.html': {'prio': '0.5', 'freq': 'monthly', 'lastmod': '2015-07-26T20:07:00+00:00'},
    'ba-03-meetup.html': {'prio': '0.5', 'freq': 'monthly', 'lastmod': '2015-08-26T20:08:00+00:00'},
    'ba-04-meetup.html': {'prio': '0.5', 'freq': 'monthly', 'lastmod': '2015-09-26T20:09:00+00:00'},
    'ba-05-meetup.html': {'prio': '0.5', 'freq': 'weekly', 'lastmod': '2015-10-26T20:10:00+00:00'},
    'thank-you.html': {'prio': '0.1', 'freq': 'yearly', 'lastmod': '2015-07-10T20:00:00+00:00'},
}


@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        g.current_lang = request.view_args['lang_code']
        if request.view_args['lang_code'] not in LANGS:
            return abort(404)
        request.view_args.pop('lang_code')


@babel.localeselector
def get_locale():
    # try to guess the language from the user accept
    # header the browser transmits. The best match wins.
    # return request.accept_languages.best_match(['de', 'sk', 'en'])
    return g.get('current_lang', app.config['BABEL_DEFAULT_LOCALE'])


def _get_template_variables(**kwargs):
    variables = {
        'title': gettext('PyCon SK'),
        'logo': LOGO_PYCON
    }
    variables.update(kwargs)

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
    return render_template('speaking.html', **_get_template_variables(li_speaking='active'))


@app.route('/<lang_code>/sponsoring.html')
def sponsoring():
    return render_template('sponsoring.html', **_get_template_variables(li_sponsoring='active'))


@app.route('/<lang_code>/tickets.html')
def tickets():
    return render_template('tickets.html', **_get_template_variables(li_tickets='active'))


@app.route('/<lang_code>/code-of-conduct.html')
def code_of_conduct():
    return render_template('code-of-conduct.html', **_get_template_variables(li_coc='active'))


@app.route('/<lang_code>/spy.html')
def spy():
    return render_template('spy.html', **_get_template_variables(title='SPy o. z.', li_spy='active'))


@app.route('/<lang_code>/thank-you.html')
def thank_you():
    return render_template('thank-you.html', **_get_template_variables())


@app.route('/<lang_code>/meetup.html')
def meetup():
    return render_template('meetup.html', **_get_template_variables(li_meetup='active'))


@app.route('/<lang_code>/ba-01-meetup.html')
def ba_meetup_01():
    return render_template('ba-01-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active'))


@app.route('/<lang_code>/ba-02-meetup.html')
def ba_meetup_02():
    return render_template('ba-02-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active'))


@app.route('/<lang_code>/ba-03-meetup.html')
def ba_meetup_03():
    return render_template('ba-03-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active'))


@app.route('/<lang_code>/ba-04-meetup.html')
def ba_meetup_04():
    return render_template('ba-04-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active'))


@app.route('/<lang_code>/ba-05-meetup.html')
def ba_meetup_05():
    return render_template('ba-05-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active'))


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    pages=[]
    # static pages
    for rule in app.url_map.iter_rules():

        if "GET" in rule.methods:
            if len(rule.arguments)==0:
                indx = rule.rule.replace('/', '')
                pages.append({
                    'loc': 'https://pycon.sk' + rule.rule,
                    'lastmod': SITEMAP[indx]['lastmod'],
                    'freq': SITEMAP[indx]['freq'],
                    'prio': SITEMAP[indx]['prio'],
                    })

            elif 'lang_code' in rule.arguments:
                indx = rule.rule.replace('/<lang_code>/', '')

                for lang in LANGS:
                    pages.append({
                        'loc': 'https://pycon.sk' + rule.rule.replace('<lang_code>', lang),
                        'lastmod': SITEMAP[indx]['lastmod'],
                        'freq': SITEMAP[indx]['freq'],
                        'prio': SITEMAP[indx]['prio'],
                        })

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response= make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


if __name__ == "__main__":
    app.run(debug=True)
