"""
@@pdfreactor-config browser: very basic configuration
"""

# Zope:
from Products.Five.browser import BrowserView
from zope.interface import implements

# Local imports:
from pdfreactor.plone.interfaces import IGetPdfReactorConversionSettings


class BaseSettingsView(BrowserView):
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

    def getZopeCookies(self):
        """
        Return the Zope cookies as expected by the PDFreactor client API

        When requesting a PDF, we'll always have those cookies!
        """
        return {
            'cookies': [{'key': key, 'value': value}
                        for (key, value) in self.request.cookies.items()
                        if key in ('__ac',    # loggedin
                                   '_ZopeId', # Zope session
                                   'I18N_LANGUAGE',
                                   )
                        ],
            }
