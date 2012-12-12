WireXfers integration with Flask
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simple demo application demonstrating WireXfers_ usage with Flask_.

.. _WireXfers: http://plaes.org/projects/wirexfers
.. _Flask: http://flask.pocoo.org/


Requirements
------------
- Flask
- PyCrypto
- WireXfers

Notes
-----

Protocols using private/public key pair require keys to be in `pem` format.
Extracting keys from certificate (`cert.pem`) using `openssl` utility::

     openssl x509 -inform pem -in cert.pem -pubkey -noout

Private key should look like this::

    -----BEGIN RSA PRIVATE KEY-----
    ...
    -----END RSA PRIVATE KEY-----

And public key like this::

    -----BEGIN PUBLIC KEY-----
    ...
    -----END PUBLIC KEY-----
