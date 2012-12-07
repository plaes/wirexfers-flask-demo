# -*- coding: utf-8 -*-
"""
    flask-pangalink
    ~~~~~~~~~~~~~~~

    Example banklink application

    :copyright: (c) 2012, Priit Laes
"""
from flask import Flask

from . import utils

def app_setup_payments(conf):
    providers = {}
    c = conf.get('PAYMENTS', {})
    for p, data in conf.get('PAYMENTS', {}).iteritems():
        providers[p] = utils.init_provider(p, data)
    return providers

class DefaultConfig(object):
    DEBUG = True
    TESTING = True
    # Payment provider configuration
    PAYMENTS = {
        # Tupas/SOLO bank
        'tupas.EENordea': {
            # Custom name
            'name': 'Nordea pank',
            # Authentication information / structure depends on the provider
            'auth': {'mac_key': 'LEHTI'},
            'user': '12345678',
            'endpoint': 'https://netbank.nordea.com/pnbepaytest/epayn.jsp'
        },
        # IPizza (TODO)
    }

# Initialize app and configuration
app = Flask(__name__)
app.config.from_object(DefaultConfig())
# Initialize payment provider configuration
app.payments = app_setup_payments(app.config)

@app.route('/')
def index():
    return 'xxx'
