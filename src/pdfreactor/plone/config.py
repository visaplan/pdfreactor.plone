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
