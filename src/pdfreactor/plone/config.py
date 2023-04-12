"""
@@pdfreactor-config browser: very basic configuration
"""

# Zope:
from Products.Five.browser import BrowserView
from zope.interface import implements

# Local imports:
from pdfreactor.plone.interfaces import IGetPdfReactorConversionSettings
from ._mixin import GimmeCookies


class BaseSettingsView(BrowserView, GimmeCookies):
    """
    Return a very basic `config` dict e.g. for PDFreactor.convert

    The most important part are the cookies, to make it possible to export
    non-public contents.
    """

    implements(IGetPdfReactorConversionSettings)

    def __call__(self):
        config = self.getZopeCookies()
        config.update({
            'integrationStyleSheets': [{
                'uri': '++resource++pdfreactor.plone/export.css',
                }],
            })
        return config


class MathjaxSettingsView(BrowserView):
    """
    Return the configuration of the Mathjax integration to use

    To process MathML input, we need to use MathJax v2
    (as of PDFreactor 11.6.2, v3 is not supported yet).
    Unless using the defaults (which means, a 'MathJax.js' script in the
    current base path), we need to initialize up to three Javascript variables.

    Make sure Javascript excecution is enabled, too!
    (config: 'javaScriptSettings': {'enabled': True})
    """

    def values(self):
        """
        This will probably use configurable values soon
        """
        return {
            'roMjPath': 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/',
            'roMjFile': 'MathJax.js',
            'roMjSvgBlacker': 0,
            }

    def text(self):
        return '\n'.join(['window.%s = %r;' % tup for tup in self.values().items()])
        return '''// see https://www.pdfreactor.com/product/doc_html/index.html#MathML
        var roMjPath = %(roMjPath)r,
            roMjFile = %(roMjFile)r,
            roMjSvgBlacker = %(roMjSvgBlacker)r;
        ''' % self.values()


    # We don't define a similar interface for the connection settings here
    # because we don't expect so much customization regarding this aspect;
    # it should be enough to
