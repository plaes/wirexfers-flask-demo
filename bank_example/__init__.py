# -*- coding: utf-8 -*-
"""
    flask-pangalink
    ~~~~~~~~~~~~~~~

    Example banklink application

    :copyright: (c) 2012, Priit Laes
"""
from flask import Flask, redirect, render_template, request, session, url_for
from wirexfers import PaymentInfo
from wirexfers.exc import InvalidResponseError
from wirexfers.utils import ref_731

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
    SECRET_KEY = 'Change me you must!'
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
        # IPizza banks
        'ipizza.EEKrediidipank': {
            'name': 'Krediidipank',
            # Authentication information for IPizza keychain
            'auth': {'private_key': 'private_key.pem', 'public_key': 'public_key.pem'},
            'user': 'uid285582',
            'endpoint': 'https://pangalink.net/banklink/008/krediidipank',
            'extra_args': {'keypath': 'data/krediidipank'},
        },
        'ipizza.EELHV': {
            'name': 'LHV Pank',
            'auth': {'private_key': 'private_key.pem', 'public_key': 'public_key.pem'},
            'user': 'uid285812',
            'endpoint': 'https://pangalink.net/banklink/008/lhv',
            'extra_args': {'keypath': 'data/lhv'},
        },
        'ipizza.EESEB': {
            'name': 'SEB Pank',
            'auth': {'private_key': 'private_key.pem', 'public_key': 'public_key.pem'},
            'user': 'uid285870',
            'endpoint': 'https://pangalink.net/banklink/008/seb',
            'extra_args': {'keypath': 'data/seb'},
        },
        'ipizza.EESwedBank': {
            'name': 'SWEDBank',
            'auth': {'private_key': 'private_key.pem', 'public_key': 'public_key.pem'},
            'user': 'uid285883',
            'endpoint': 'https://pangalink.net/banklink/008/swedbank',
            'extra_args': {'keypath': 'data/swedbank'},
        },
    }

# Initialize app and configuration
app = Flask(__name__)
app.config.from_object(DefaultConfig())
# Initialize payment provider configuration
app.providers = app_setup_payments(app.config)

@app.route('/')
def index():
    # Teoorias peaks juba siin tekitama PaymentInfo, aga kuna me baasi ei
    # kasuta, siis teeme seda alles peale seda kui kasutaja on panga valinud.
    return render_template('index.html', providers=app.providers)

@app.route('/payment/', methods=['POST'])
def payment():
    bank = request.args.get('bank', None)
    # Do some basic error checking
    if not bank or bank not in app.providers:
        return redirect(url_for('index'))
    # Set up payment information (amount, description and reference no.)
    payment_info = PaymentInfo('6.66', 'Payment info', ref_731('123456'))
    # Set up return urls
    urls = {'return': url_for('finish', _external=True)}
    # Do bank-specific handling (ie. Tupas/SOLO has extra return urls)
    if bank.startswith('tupas'):
        urls['reject'] = url_for('finish', result='cancel', _external=True)
        urls['cancel'] = url_for('finish', result='reject', _external=True)
    # Save bank id in session (comes in handy when processing returns)
    session['bank'] = bank
    return render_template('form.html', payment=app.providers[bank](payment_info, urls))

@app.route('/finish', methods=['GET', 'POST'])
def finish():
    # Handle iso8859-1 responses (Stupid Danske bank)
    request.encoding_errors = 'fallback:latin'

    # Check whether we have provider id in session (we should also check whether order is the same)
    bank = session.get('bank', None)
    if not bank or bank not in app.providers:
        # Redirect to error page
        return redirect(url_for('index'))

    # TODO: handle Nordea-specific URLs (reject, cancel)
    # if 'reject' in request.args:
    #     return redirect(url_for(...))
    # if 'cancel in request.args:
    #     return redirect(url_for(...))

    # Handle payment response
    data = request.args if request.method == 'GET' else request.form
    del session['bank']
    try:
        response = app.providers[bank].parse_response(data)
    except InvalidResponseError:
        return redirect(url_for('invalid'))

    # If required, store extra order info
    # order.info = response.data

    if response.successful:
        return redirect(url_for('success'))
    return redirect(url_for('reject'))

@app.route('/invalid')
def invalid():
    return 'Invalid payment information'

@app.route('/success')
def success():
    return 'Payment was successful'

@app.route('/reject')
def reject():
    return 'Payment was rejected (by bank?)'
