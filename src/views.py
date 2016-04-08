#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from datetime import datetime
from flask import Flask, g, request, send_from_directory, render_template, abort, make_response
from flask.ext.babel import Babel, gettext

app = Flask(__name__, static_url_path='/static')
app.config['BABEL_DEFAULT_LOCALE'] = 'sk'
app.jinja_options = {'extensions': ['jinja2.ext.with_', 'jinja2.ext.i18n']}
babel = Babel(app)

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
LOGO_PYCON = 'images/logo/pycon.svg'
LOGO_MEETUP_BA = 'images/logo/bratislava_logo.svg'

LANGS = ('en', 'sk')
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+00:00'
NOW = datetime.utcnow().strftime(TIME_FORMAT)


def get_mtime(filename):
    mtime = datetime.fromtimestamp(os.path.getmtime(filename))
    return mtime.strftime(TIME_FORMAT)


SITEMAP_DEFAULT = {'prio': '0.1', 'freq': 'weekly'}
SITEMAP = {
    'sitemap.xml': {'prio': '0.9', 'freq': 'daily', 'lastmod': get_mtime(__file__)},
    'index.html': {'prio': '1', 'freq': 'daily'},
    'tickets.html': {'prio': '0.1', 'freq': 'weekly'},
    'speakers.html': {'prio': '0.4', 'freq': 'weekly'},
    'sponsors.html': {'prio': '0.4', 'freq': 'weekly'},
    'code-of-conduct.html': {'prio': '0.9', 'freq': 'weekly'},
    'schedule-friday.html': {'prio': '0.5', 'freq': 'weekly'},
    'schedule-saturday.html': {'prio': '0.5', 'freq': 'weekly'},
    'schedule-sunday.html': {'prio': '0.5', 'freq': 'weekly'},
    'pod-zastitou-prezidenta-slovenskej-republiky.html': {'prio': '0.5', 'freq': 'weekly'},
    'spy.html': {'prio': '0.75', 'freq': 'weekly'},
    'stats-web.html': {'prio': '0.8', 'freq': 'weekly'},
    'stats-slido.html': {'prio': '0.8', 'freq': 'weekly'},
    'photos.html': {'prio': '0.8', 'freq': 'weekly'},
    'videos.html': {'prio': '0.8', 'freq': 'weekly'},
    'getting-here.html': {'prio': '0.2', 'freq': 'weekly'},
    'django-girls.html': {'prio': '0.2', 'freq': 'weekly'},
    'meetup.html': {'prio': '0.6', 'freq': 'weekly'},
    'console.html': {'prio': '0.3', 'freq': 'weekly'},
    'speaking.html': {'prio': '0.1', 'freq': 'weekly'},
    'sponsoring.html': {'prio': '0.1', 'freq': 'weekly'},
}
LDJSON = {
    "@context": "http://schema.org",
    "@type": "Organization",
    "name": "PyCon SK",
    "url": "https://2016.pycon.sk",
    "logo": "https://2016.pycon.sk/static/images/pycon_sk_logo200_notext.png",
    "sameAs": [
      "https://facebook.com/pyconsk",
      "https://twitter.com/pyconsk",
      "https://www.linkedin.com/company/spy-o--z-",
      "https://github.com/pyconsk",
      "https://pyconsk.slack.com"
    ]
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
        'logo': LOGO_PYCON,
        'ld_json': LDJSON
    }
    variables.update(kwargs)

    if 'current_lang' in g:
        variables['lang_code'] = g.current_lang
    else:
        variables['lang_code'] = app.config['BABEL_DEFAULT_LOCALE']

    return variables


@app.route('/<lang_code>/index.html')
def index():
    lang =  get_locale()
    LDJSON_EVENT = {
      "@context": "http://schema.org",
      "@type": "Event",
      "name": u"PyCon SK 2016",
      "startDate": "2016-03-11T9:00:00+01:00",
      "endDate" : "2016-03-13T18:00:00+01:00",
      "url": "https://2016.pycon.sk/"+ lang +"/",
      "sameAs": [
        "https://www.facebook.com/events/941546202585736/"
      ],
      "offers": [{
        "@type" : "Offer",
        "name" : "Supporter Early Bird",
        "category" : "presale",
        "price" : "70",
        "priceCurrency" : "EUR",
        "url" : "https://ti.to/pyconsk/2016"
      },{
        "@type" : "Offer",
        "name" : "Standard Early Bird",
        "category" : "presale",
        "price" : "30",
        "priceCurrency" : "EUR",
        "url" : "https://ti.to/pyconsk/2016"
      },{
        "@type" : "Offer",
        "name" : "Student Early Bird",
        "category" : "presale",
        "price" : "15",
        "priceCurrency" : "EUR",
        "url" : "https://ti.to/pyconsk/2016"
      }],
      "workPerformed": {
        "@type": "CreativeWork",
        "name": "PyCon SK 2016",
        "creator": {
          "@type": "Organization",
          "name": "SPy o.z.",
          "url": "https://pycon.sk/"+ lang +"/spy.html",
          "logo": "https://pycon.sk/static/images/pycon_sk_logo200_notext.png",
          "sameAs": [
            "https://facebook.com/pyconsk",
            "https://twitter.com/pyconsk",
            "https://www.linkedin.com/company/spy-o--z-",
            "https://github.com/pyconsk",
            "https://pyconsk.slack.com"
          ],
        }
      }
    }
    return render_template('index.html', **_get_template_variables(ld_json=LDJSON_EVENT, li_index='active'))


@app.route('/<lang_code>/console.html')
def console():
    return render_template('console.html', **_get_template_variables(li_console='active'))


@app.route('/<lang_code>/speakers.html')
def speakers():
    return render_template('speakers.html', **_get_template_variables(li_speaking='active'))


@app.route('/<lang_code>/speaking.html')
def speaking():
    return render_template('speaking.html', **_get_template_variables(li_speaking='active'))

@app.route('/<lang_code>/sponsors.html')
def sponsors():
    return render_template('sponsors.html', **_get_template_variables(li_sponsoring='active'))


@app.route('/<lang_code>/sponsoring.html')
def sponsoring():
    return render_template('sponsoring.html', **_get_template_variables(li_sponsoring='active'))


@app.route('/<lang_code>/tickets.html')
def tickets():
    return render_template('tickets.html', **_get_template_variables(li_tickets='active'))


@app.route('/<lang_code>/getting-here.html')
def getting_here():
    return render_template('getting-here.html', **_get_template_variables(li_getting_here='active'))


@app.route('/<lang_code>/code-of-conduct.html')
def code_of_conduct():
    return render_template('code-of-conduct.html', **_get_template_variables(li_coc='active'))


@app.route('/<lang_code>/schedule-friday.html')
def schedule_fri():
    return render_template('schedule-friday.html', **_get_template_variables(
        li_schedule='active',
        li_schedule_fri='active'
    ))


@app.route('/<lang_code>/schedule-saturday.html')
def schedule_sat():
    return render_template('schedule-saturday.html', **_get_template_variables(
        li_schedule='active',
        li_schedule_sat='active'
    ))


@app.route('/<lang_code>/schedule-sunday.html')
def schedule_sun():
    return render_template('schedule-sunday.html', **_get_template_variables(
        li_schedule='active',
        li_schedule_sun='active'
    ))


@app.route('/<lang_code>/pod-zastitou-prezidenta-slovenskej-republiky.html')
def president():
    return render_template('pod-zastitou-prezidenta-slovenskej-republiky.html', **_get_template_variables(li_index='active'))


@app.route('/<lang_code>/photos.html')
def photos():
    return render_template('photos.html', **_get_template_variables(li_index='active', li_photos='active'))


@app.route('/<lang_code>/videos.html')
def videos():
    return render_template('videos.html', **_get_template_variables(li_index='active', li_videos='active'))


@app.route('/<lang_code>/stats-web.html')
def stats_web():
    return render_template('stats-web.html', **_get_template_variables(li_index='active', li_stats_web='active'))


@app.route('/<lang_code>/stats-slido.html')
def stats_slido():
    return render_template('stats-slido.html', **_get_template_variables(li_index='active', li_stats_slido='active'))


@app.route('/<lang_code>/spy.html')
def spy():
    lang =  get_locale()
    LDJSON = {
        "@context": "http://schema.org",
        "@type": "Organization",
        "name": "SPy o.z.",
        "url": "https://pycon.sk/"+ lang +"/spy.html",
        "logo": "https://pycon.sk/static/images/pycon_sk_logo200_notext.png",
        "sameAs": [
          "https://facebook.com/pyconsk",
          "https://twitter.com/pyconsk",
          "https://www.linkedin.com/company/spy-o--z-",
          "https://github.com/pyconsk",
          "https://pyconsk.slack.com"
        ]
    }
    return render_template('spy.html', **_get_template_variables(title='SPy o.z.', li_spy='active',
                                                                          ld_json=LDJSON))


@app.route('/<lang_code>/thank-you.html')
def thank_you():
    return render_template('thank-you.html', **_get_template_variables())


@app.route('/<lang_code>/django-girls.html')
def django_girls():
    return render_template('django-girls.html', **_get_template_variables(li_workshop='active'))


@app.route('/<lang_code>/meetup.html')
def meetup():
    return render_template('meetup.html', **_get_template_variables(li_meetup='active'))


@app.route('/<lang_code>/ba-01-meetup.html')
def ba_meetup_01():
    lang =  get_locale()
    LDJSON_EVENT = {
      "@context": "http://schema.org",
      "@type": "Event",
      "name": u"Prvý Bratislavský Python Meetup",
      "startDate": "2015-07-07T18:00:00+01:00",
      "endDate" : "2015-07-07T22:00:00+01:00",
      "url": "https://pycon.sk/"+ lang +"/ba-01-meetup.html",
      "sameAs": [
        "https://www.facebook.com/events/800093356777151/",
        "http://lanyrd.com/2015/pyba/"
      ],
      "location": {
        "@type": "Place",
        "sameAs": "https://progressbar.sk",
        "name": "Progressbar",
        "address": u"Michalská 3, Bratislava"
      },
      "offers": {
        "@type": "Offer",
        "price": 0,
        "priceCurrency": "EUR"
      },
      "performer": [{
        "@type": "Person",
        "name": u"Filip Kłębczyk",
        "sameAs": "https://pl.linkedin.com/in/fklebczyk"
        },{
        "@type": "Person",
        "name": u"Daniel Kontšek",
        "sameAs": "https://sk.linkedin.com/in/danielkontsek"
        },{
        "@type": "Person",
        "name": "Richard Kellner",
        "sameAs": "https://sk.linkedin.com/in/richardkellner"
        }
      ],
      "workPerformed": {
        "@type": "CreativeWork",
        "name": u"Prvý Bratislavský Python Meetup",
        "creator": [{
          "@type": "Person",
          "name": "Richard Kellner",
          "sameAs": "https://sk.linkedin.com/in/richardkellner"
          },{
          "@type": "Person",
          "name": u"Daniel Kontšek",
          "sameAs": "https://sk.linkedin.com/in/danielkontsek"
          }
        ]
      }
    }
    return render_template('ba-01-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active',
                                                                          ld_json=LDJSON_EVENT))


@app.route('/<lang_code>/ba-02-meetup.html')
def ba_meetup_02():
    lang =  get_locale()
    LDJSON_EVENT = {
      "@context": "http://schema.org",
      "@type": "Event",
      "name": u"Druhý Bratislavský Python Meetup",
      "startDate": "2015-08-04T18:00:00+01:00",
      "endDate" : "2015-08-04T22:00:00+01:00",
      "url": "https://pycon.sk/"+ lang +"/ba-02-meetup.html",
      "sameAs": [
        "https://www.facebook.com/events/405531022976000/",
        "http://lanyrd.com/2015/pyconsk/"
      ],
      "location": {
        "@type": "Place",
        "sameAs": "https://progressbar.sk",
        "name": "Progressbar",
        "address": u"Michalská 3, Bratislava"
      },
      "offers": {
        "@type": "Offer",
        "price": 0,
        "priceCurrency": "EUR"
      },
      "performer": [{
        "@type": "Person",
        "name": u"Daniel Kontšek",
        "sameAs": "https://sk.linkedin.com/in/danielkontsek"
        },{
        "@type": "Person",
        "name": "Richard Kellner",
        "sameAs": "https://sk.linkedin.com/in/richardkellner"
        }
      ],
      "workPerformed": {
        "@type": "CreativeWork",
        "name": u"Druhý Bratislavský Python Meetup",
        "creator": [{
          "@type": "Person",
          "name": "Richard Kellner",
          "sameAs": "https://sk.linkedin.com/in/richardkellner"
          },{
          "@type": "Person",
          "name": u"Daniel Kontšek",
          "sameAs": "https://sk.linkedin.com/in/danielkontsek"
          }
        ]
      }
    }
    return render_template('ba-02-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active',
                                                                          ld_json=LDJSON_EVENT))


@app.route('/<lang_code>/ba-03-meetup.html')
def ba_meetup_03():
    lang =  get_locale()
    LDJSON_EVENT = {
      "@context": "http://schema.org",
      "@type": "Event",
      "name": u"Tretí Bratislavský Python Meetup",
      "startDate": "2015-09-08T18:00:00+01:00",
      "endDate" : "2015-09-08T22:00:00+01:00",
      "url": "https://pycon.sk/"+ lang +"/ba-03-meetup.html",
      "sameAs": [
        "https://www.facebook.com/events/860134137403420/",
        "http://lanyrd.com/2015/bratislava-python-meetup-3/"
      ],
      "location": {
        "@type": "Place",
        "sameAs": "https://progressbar.sk",
        "name": "Progressbar",
        "address": u"Michalská 3, Bratislava"
      },
      "offers": {
        "@type": "Offer",
        "price": 0,
        "priceCurrency": "EUR"
      },
      "performer": [{
        "@type": "Person",
        "name": u"Tomáš Pytel",
        "sameAs": "https://sk.linkedin.com/in/tomáš-pytel-80956698"
        }
      ],
      "workPerformed": {
        "@type": "CreativeWork",
        "name": u"Tretí Bratislavský Python Meetup",
        "creator": [{
          "@type": "Person",
          "name": "Richard Kellner",
          "sameAs": "https://sk.linkedin.com/in/richardkellner"
          },{
          "@type": "Person",
          "name": u"Daniel Kontšek",
          "sameAs": "https://sk.linkedin.com/in/danielkontsek"
          }
        ]
      }
    }
    return render_template('ba-03-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active',
                                                                          ld_json=LDJSON_EVENT))


@app.route('/<lang_code>/ba-04-meetup.html')
def ba_meetup_04():
    lang =  get_locale()
    LDJSON_EVENT = {
      "@context": "http://schema.org",
      "@type": "Event",
      "name": u"Štvrtý Bratislavský Python Meetup",
      "startDate": "2015-10-06T18:00:00+01:00",
      "endDate" : "2015-10-06T22:00:00+01:00",
      "url": "https://pycon.sk/"+ lang +"/ba-04-meetup.html",
      "sameAs": "https://www.facebook.com/events/1003712976319521/",
      "location": {
        "@type": "Place",
        "sameAs": "https://progressbar.sk",
        "name": "Progressbar",
        "address": u"Michalská 3, Bratislava"
      },
      "offers": {
        "@type": "Offer",
        "price": 0,
        "priceCurrency": "EUR"
      },
      "performer": {
        "@type": "Person",
        "name": u"Adam Števko",
        "sameAs": "https://sk.linkedin.com/in/xenol"
      },
      "workPerformed": {
        "@type": "CreativeWork",
        "name": u"Štvrtý Bratislavský Python Meetup",
        "creator": {
          "@type": "Organization",
          "name": "SPy o.z.",
          "url": "https://pycon.sk/"+ lang +"/spy.html",
          "logo": "https://pycon.sk/static/images/pycon_sk_logo200_notext.png",
          "sameAs": [
            "https://facebook.com/pyconsk",
            "https://twitter.com/pyconsk",
            "https://www.linkedin.com/company/spy-o--z-",
            "https://github.com/pyconsk",
            "https://pyconsk.slack.com"
          ],
        }
      }
    }
    return render_template('ba-04-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active',
                                                                          ld_json=LDJSON_EVENT))


@app.route('/<lang_code>/ba-05-meetup.html')
def ba_meetup_05():
    lang =  get_locale()
    LDJSON_EVENT = {
      "@context": "http://schema.org",
      "@type": "Event",
      "name": u"Piaty Bratislavský Python Meetup",
      "startDate": "2015-11-10T18:00:00+01:00",
      "endDate" : "2015-11-10T22:00:00+01:00",
      "url": "https://pycon.sk/"+ lang +"/ba-05-meetup.html",
      "sameAs": "https://www.facebook.com/events/850999828331493/",
      "location": {
        "@type": "Place",
        "sameAs": "https://progressbar.sk",
        "name": "Progressbar",
        "address": u"Michalská 3, Bratislava"
      },
      "offers": {
        "@type": "Offer",
        "price": 0,
        "priceCurrency": "EUR"
      },
      "performer": [{
        "@type": "Person",
        "name": "Richard Kellner",
        "sameAs": "https://sk.linkedin.com/in/richardkellner"
        }
      ],
      "workPerformed": {
        "@type": "CreativeWork",
        "name": u"Piaty Bratislavský Python Meetup",
        "creator": {
          "@type": "Organization",
          "name": "SPy o.z.",
          "url": "https://pycon.sk/"+ lang +"/spy.html",
          "logo": "https://pycon.sk/static/images/pycon_sk_logo200_notext.png",
          "sameAs": [
            "https://facebook.com/pyconsk",
            "https://twitter.com/pyconsk",
            "https://www.linkedin.com/company/spy-o--z-",
            "https://github.com/pyconsk",
            "https://pyconsk.slack.com"
          ],
        }
      }
    }
    return render_template('ba-05-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active',
                                                                          ld_json=LDJSON_EVENT))


@app.route('/<lang_code>/ba-06-meetup.html')
def ba_meetup_06():
    lang =  get_locale()
    LDJSON_EVENT = {
      "@context": "http://schema.org",
      "@type": "Event",
      "name": u"Šiesty Bratislavský Python Meetup",
      "startDate": "2015-12-08T18:00:00+01:00",
      "endDate" : "2015-12-08T22:00:00+01:00",
      "url": "https://pycon.sk/"+ lang +"/ba-06-meetup.html",
      "sameAs": "https://www.facebook.com/events/1686942358205368/",
      "location": {
        "@type": "Place",
        "sameAs": "https://progressbar.sk",
        "name": "Progressbar",
        "address": u"Michalská 3, Bratislava"
      },
      "offers": {
        "@type": "Offer",
        "price": 0,
        "priceCurrency": "EUR"
      },
      "performer": [{
        "@type": "Person",
        "name": u"Juraj Bubniak",
        "sameAs": "https://sk.linkedin.com/in/jurajbubniak"
        }
      ],
      "workPerformed": {
        "@type": "CreativeWork",
        "name": u"Šiesty Bratislavský Python Meetup",
        "creator": {
          "@type": "Organization",
          "name": "SPy o.z.",
          "url": "https://pycon.sk/"+ lang +"/spy.html",
          "logo": "https://pycon.sk/static/images/pycon_sk_logo200_notext.png",
          "sameAs": [
            "https://facebook.com/pyconsk",
            "https://twitter.com/pyconsk",
            "https://www.linkedin.com/company/spy-o--z-",
            "https://github.com/pyconsk",
            "https://pyconsk.slack.com"
          ],
        }
      }
    }
    return render_template('ba-06-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active',
                                                                          ld_json=LDJSON_EVENT))


@app.route('/<lang_code>/ba-07-meetup.html')
def ba_meetup_07():
    lang =  get_locale()
    LDJSON_EVENT = {
      "@context": "http://schema.org",
      "@type": "Event",
      "name": u"Siedmy Bratislavský Python Meetup",
      "startDate": "2016-01-12T18:00:00+01:00",
      "endDate" : "2016-01-12T22:00:00+01:00",
      "url": "https://pycon.sk/"+ lang +"/ba-07-meetup.html",
      "sameAs": "https://www.facebook.com/events/1686942358205368/",
      "location": {
        "@type": "Place",
        "sameAs": "https://progressbar.sk",
        "name": "Progressbar",
        "address": u"Michalská 3, Bratislava"
      },
      "offers": {
        "@type": "Offer",
        "price": 0,
        "priceCurrency": "EUR"
      },
      "performer": [{
        "@type": "Person",
        "name": u"Andrej Mošať",
        "sameAs": "https://sk.linkedin.com/in/mosat"
        }
      ],
      "workPerformed": {
        "@type": "CreativeWork",
        "name": u"Siedmy Bratislavský Python Meetup",
        "creator": {
          "@type": "Organization",
          "name": "SPy o.z.",
          "url": "https://pycon.sk/"+ lang +"/spy.html",
          "logo": "https://pycon.sk/static/images/pycon_sk_logo200_notext.png",
          "sameAs": [
            "https://facebook.com/pyconsk",
            "https://twitter.com/pyconsk",
            "https://www.linkedin.com/company/spy-o--z-",
            "https://github.com/pyconsk",
            "https://pyconsk.slack.com"
          ],
        }
      }
    }
    return render_template('ba-07-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active',
                                                                          ld_json=LDJSON_EVENT))


@app.route('/<lang_code>/ba-08-meetup.html')
def ba_meetup_08():
    lang =  get_locale()
    LDJSON_EVENT = {
      "@context": "http://schema.org",
      "@type": "Event",
      "name": u"Ôsmy Bratislavský Python Meetup",
      "startDate": "2016-02-09T18:00:00+01:00",
      "endDate" : "2016-02-09T22:00:00+01:00",
      "url": "https://pycon.sk/"+ lang +"/ba-08-meetup.html",
      "sameAs": "https://www.facebook.com/events/110990379283146/",
      "location": {
        "@type": "Place",
        "sameAs": "https://progressbar.sk",
        "name": "Progressbar",
        "address": u"Michalská 3, Bratislava"
      },
      "offers": {
        "@type": "Offer",
        "price": 0,
        "priceCurrency": "EUR"
      },
      "performer": [{
        "@type": "Person",
        "name": u"Miroslav Beka",
        "sameAs": "https://github.com/mirobeka"
        }
      ],
      "workPerformed": {
        "@type": "CreativeWork",
        "name": u"Ôsmy Bratislavský Python Meetup",
        "creator": {
          "@type": "Organization",
          "name": "SPy o.z.",
          "url": "https://pycon.sk/"+ lang +"/spy.html",
          "logo": "https://pycon.sk/static/images/pycon_sk_logo200_notext.png",
          "sameAs": [
            "https://facebook.com/pyconsk",
            "https://twitter.com/pyconsk",
            "https://www.linkedin.com/company/spy-o--z-",
            "https://github.com/pyconsk",
            "https://pyconsk.slack.com"
          ],
        }
      }
    }
    return render_template('ba-08-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active',
                                                                          ld_json=LDJSON_EVENT))

@app.route('/<lang_code>/ba-09-meetup.html')
def ba_meetup_09():
    lang =  get_locale()
    LDJSON_EVENT = {
      "@context": "http://schema.org",
      "@type": "Event",
      "name": u"Deviaty Bratislavský Python Meetup",
      "startDate": "2016-04-12T18:00:00+01:00",
      "endDate" : "2016-04-12T21:00:00+01:00",
      "url": "https://pycon.sk/"+ lang +"/ba-09-meetup.html",
#      "sameAs": "https://www.facebook.com/events/110990379283146/",
      "location": {
        "@type": "Place",
        "sameAs": "https://progressbar.sk",
        "name": "Progressbar",
        "address": u"Michalská 3, Bratislava"
      },
      "offers": {
        "@type": "Offer",
        "price": 0,
        "priceCurrency": "EUR"
      },
#      "performer": [{
#        "@type": "Person",
#        "name": u"Richard Kellner",
#        "sameAs": "https://github.com/"
#        }
#      ],
      "workPerformed": {
        "@type": "CreativeWork",
        "name": u"Deviaty Bratislavský Python Meetup",
        "creator": {
          "@type": "Organization",
          "name": "SPy o.z.",
          "url": "https://pycon.sk/"+ lang +"/spy.html",
          "logo": "https://pycon.sk/static/images/pycon_sk_logo200_notext.png",
          "sameAs": [
            "https://facebook.com/pyconsk",
            "https://twitter.com/pyconsk",
            "https://www.linkedin.com/company/spy-o--z-",
            "https://github.com/pyconsk",
            "https://pyconsk.slack.com"
          ],
        }
      }
    }
    return render_template('ba-09-meetup.html', **_get_template_variables(logo=LOGO_MEETUP_BA, li_meetup='active',
                                                                          ld_json=LDJSON_EVENT))


@app.route('/<lang_code>/ba-09-meetup-slides.html')
def ba_meetup_09_slides():
    return render_template('ba-09-meetup-slides.html', **_get_template_variables())


def get_lastmod(route, sitemap_entry):
    """Used by sitemap() below"""
    if 'lastmod' in sitemap_entry:
        return sitemap_entry['lastmod']

    template = route.rule.split('/')[-1]
    template_file = os.path.join(SRC_DIR, 'templates', template)

    if os.path.exists(template_file):
        return get_mtime(template_file)

    return NOW


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    domain = 'https://2016.pycon.sk'
    pages = []

    # static pages
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            if len(rule.arguments) == 0:
                indx = rule.rule.replace('/', '')
                sitemap_data = SITEMAP.get(indx, SITEMAP_DEFAULT)
                pages.append({
                    'loc': domain + rule.rule,
                    'lastmod': get_lastmod(rule, sitemap_data),
                    'freq': sitemap_data['freq'],
                    'prio': sitemap_data['prio'],
                })

            elif 'lang_code' in rule.arguments:
                indx = rule.rule.replace('/<lang_code>/', '')

                for lang in LANGS:
                    alternate = []

                    for alt_lang in LANGS:
                        if alt_lang != lang:
                            alternate.append({
                                'lang': alt_lang,
                                'url': domain + rule.rule.replace('<lang_code>', alt_lang)
                            })

                    sitemap_data = SITEMAP.get(indx, SITEMAP_DEFAULT)
                    pages.append({
                        'loc': domain + rule.rule.replace('<lang_code>', lang),
                        'alternate': alternate,
                        'lastmod': get_lastmod(rule, sitemap_data),
                        'freq': sitemap_data['freq'],
                        'prio': sitemap_data['prio'],
                    })

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response= make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


if __name__ == "__main__":
    app.run(debug=True, host=os.environ.get('FLASK_HOST', '127.0.0.1'), port=int(os.environ.get('FLASK_PORT', 5000)))
