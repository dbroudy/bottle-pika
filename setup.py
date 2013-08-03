from setuptools import setup
import os

# This ugly hack executes the first few lines of the module file to look up some
# common variables. We cannot just import the module because it depends on other
# modules that might not be installed yet.
filename = os.path.join(os.path.dirname(__file__), 'bottle_pika.py')
source = open(filename).read().split('### CUT HERE')[0]
exec(source)

setup(
    name = 'bottle_pika',
    version = __version__,
    url = 'https://github.com/dbroudy/bottle-pika',
    description = 'Pika plugin module for Bottle microframework',
    long_description = __doc__,
    keywords = 'bottle rabbitmq amqp pika messaging message queue',
    author = 'David Broudy',
    author_email = 'dave@broudy.net',
    license = __license__,
    platforms = 'any',
    py_modules = [ 'bottle_pika' ],
    classifiers = [
      'Development Status :: 4 - Beta',
      'Environment :: Web Environment',
      'Framework :: Bottle',
      'Operating System :: OS Independent',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires = [
      'bottle >= 0.10',
      'pika >= 0.9.13',
    ],
)
