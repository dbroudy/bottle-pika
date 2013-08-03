'''
Bottle-Pika is a plugin that integrates Pika (AMQP) with your Bottle
application. It automatically connects to AMQP at the beginning of a
request, passes the channel to the route callback and closes the
connection and channel afterwards.

To automatically detect routes that need a channel, the plugin
searches for route callbacks that require a `mq` keyword argument
(configurable) and skips routes that do not. This removes any overhead for
routes that don't need a message queue.

Results are returned as dictionaries.

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
'''

__version__ = '0.1.0'
__license__ = 'MIT'

### CUT HERE (see setup.py)

import inspect
import pika
from bottle import HTTPResponse, HTTPError, PluginError

class PikaPlugin(object):
    '''
    This plugin passes a amqp channel to route callbacks
    that accept a `mq` keyword argument. If a callback does not expect
    such a parameter, no connection is made. You can override the connection
    settings on a per-route basis.
    '''
    def __init__(self, params, keyword='mq'):
         self.params = params
         self.keyword = keyword

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, PikaPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another pika plugin with conflicting settings (non-unique keyword).")

    def apply(self, callback, context):
        # Override global configuration with route-specific values.
        conf = context['config'].get('pika') or {}
        params = conf.get('params', self.params)
        keyword = conf.get('keyword', self.keyword)

        # Test if the original callback accepts the keyword.
        # Ignore it if it does not need a channel.
        args = inspect.getargspec(context['callback'])[0]
        if keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            # Connect to the amqp instance
            con = None
            try:
                con = pika.BlockingConnection(params)
                mq = con.channel()
            except HTTPResponse, e:
                raise HTTPError(500, "AMQP Error", e)

            # Add the channel as a keyword argument.
            kwargs[keyword] = mq

            try:
                rv = callback(*args, **kwargs)
            except HTTPError, e:
                raise
            except HTTPResponse, e:
                raise
            finally:
                if con:
                    con.close()
            return rv

        # Replace the route callback with the wrapped one.
        return wrapper

Plugin = PikaPlugin
