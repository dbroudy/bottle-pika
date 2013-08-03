bottle-pika
===========

Pika is a AMQP client library for Python, used for connecting to a RabbitMQ (or other AMQP compatible) server.

Bottle-Pika is a plugin that integrates Pika (AMQP) with your Bottle
application. It automatically connects to AMQP at the beginning of a
request, passes the channel to the route callback and closes the
connection and channel afterwards.

To automatically detect routes that need a channel, the plugin
searches for route callbacks that require a `mq` keyword argument
(configurable) and skips routes that do not. This removes any overhead for
routes that don't need a message queue.

This plugin was originally based on the bottle-mysql plugin found at:
  https://pypi.python.org/pypi/bottle-mysql

Installation
===============

Install using pip:

    $ pip install bottle-pika

or download the latest version from github:

    $ git clone https://github.com/dbroudy/bottle-pika.git
    $ cd bottle-pika
    $ python setup.py install

Usage
===============

Usage Example::

    import bottle
    import bottle_pika
    import pika

    app = bottle.Bottle()
    pika_plugin = bottle_pika.Plugin(pika.URLParameters('amqp://localhost/'))
    app.install(pika_plugin)

    @app.route('/hello')
    def hello(mq):
        mq.basic_publish(...)
        return HTTPResponse(status=200)

See pika documentation on channels for more information:
  http://pika.readthedocs.org/en/latest/modules/channel.html#pika.channel.Channel

Configuration
===============

The plugin is configured by passing either a pika.ConnectionParameters or pika.URLParameters 
instance to the plugin.

You can override these on a per-route basis: 

    @app.route('/cache/<item>', pika={'params': pika.URLConnection()})
    def cache(item, mq):
        ...
   
or install two plugins with different ``keyword`` settings to the same application:

    app = bottle.Bottle()
    local_mq = bottle_pika.Plugin(params=..., keyword='local_mq')
    prod_mq = bottle_pika.Plugin(params=..., keyword='remote_mq')
    app.install(local_mq)
    app.install(prod_mq)

    @app.route('/show/<item>')
    def show(item, local_mq):
        ...

    @app.route('/cache/<item>')
    def cache(item, remote_mq):
        ...
