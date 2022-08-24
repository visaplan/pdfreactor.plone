"""
pdfreactor.plone._mixin: methods for both @@pdfreactor-config and @@as.pdf
"""

class GimmeCookies:
    """
    Provide method(s) common to several browsers

    The getZopeCookies method is not actually used in the Exporter class
    (because we use the @@pdfreactor-config view in the conversionSettings;
    this view does use it in its __call__ method).

    But you might want to use it in a derived view class which operates on the
    same objects, e.g. to create screenshots.
    """
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
