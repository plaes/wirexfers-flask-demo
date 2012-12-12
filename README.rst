Sample WireXfers integration with Flask
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simple demo application demonstrating WireXfers_ usage with Flask_.
Written by `Priit Laes`_ and sponsored by Povi_.

.. _Flask: http://flask.pocoo.org
.. _Povi: http://povi.ee
.. _Priit Laes: http://plaes.org
.. _WireXfers: http://plaes.org/projects/wirexfers

Requirements
------------

- Flask
- PyCrypto
- WireXfers

Notes
-----

IPizza payments are done against pangalink.net_ test service, mainly because
most banks lack testing services (indeed, they do!).

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

.. _pangalink.net: http://pangalink.net
