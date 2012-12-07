# -*- coding: utf-8 -*-
"""
    flask-pangalink.utils
    ~~~~~~~~~~~~~~~~~~~~~

    Simple common util functions

    :copyright: (c) 2012, Priit Laes
"""
import os

from werkzeug.utils import import_string
from wirexfers.utils import load_key

def init_provider(cls, data):
    """
    Helper utility to initialize payment providers from Flask configuration.
    """

    p = import_string('wirexfers.providers.%sProvider' % cls)
    if cls.startswith('ipizza'):
        def _load(k):
            return load_key(os.path.join(data['extra_args']['keypath'], \
                                         data['auth']['%s_key' % k]))
        keychain = p.KeyChain(_load('private'), _load('public'))
    elif cls.startswith('tupas'):
        keychain = p.KeyChain(**data['auth'])
    else:
        raise RuntimeError('Unknown payment provider: %s' % cls)
    return p(data['user'], keychain, data['endpoint'])
