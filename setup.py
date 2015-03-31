from distutils.core import setup
setup(
  name = 'shipwire',
  packages = ['shipwire'], # this must be the same as the name above
  version = '0.8.8',
  description = 'A Python abstraction layer around the Shipwire API.',
  author = 'Neil Durbin, John Coogan, Clark Fischer',
  author_email = 'neildurbin@gmail.com',
  url = 'https://github.com/soylentme/shipwire-python', # use the URL to the github repo
  download_url = 'https://github.com/soylentme/shipwire-python/archive/master.tar.gz', # I'll explain this in a second
  keywords = ['shipwire', 'api', 'wrapper', 'soylent'], # arbitrary keywords
  classifiers = [],
  install_requires = ['requests >= 2.4.3'],
)
