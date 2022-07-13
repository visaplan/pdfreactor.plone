"""
@@as.pdf browser: simple PDF export
"""

# PDFreactor (by RealObjects; Python integration by visaplan GmbH):
from pdfreactor.api import PDFreactor

# Zope:
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.interface import implements

# Local imports:
from pdfreactor.plone.interfaces import (
    IExporter,
    IPdfReactorConnectionSettings,
    )


class Exporter(BrowserView):

    implements(IExporter)

    def __init__(self, context, request):
        """
        Create the browser view, using the configured connection settings
        """
        super(Exporter, self).__init__(context, request)
        self.reactor = self.make_reactor(context)

    def make_reactor(self, context):
        """
        Create the PDFreactor object which we'll use for our conversions
        """
        registry = getToolByName(context, 'portal_registry')
        proxy = registry.forInterface(IPdfReactorConnectionSettings)
        url = proxy.service_url or None
        reactor = PDFreactor(url)
        key = proxy.api_key or None
        if key is not None and key.strip() != 'None':
            reactor.apiKey = key
        return reactor

    def conversionSettings(self):
        """
        Create the config dictionary, as expected e.g. by the PDFreactor.convert
        method.

        There are two options to customize this:

        - Inherit from this class and override the conversionSettings method.
          This might be necessary e.g. if you need to support additional
          configuration syntax, and for sure if you need to tolerate "unused"
          statements.
        - Override the 'pdfreactor-config' browser.
          Have a look at the pdfreactor.parsecfg package for a browser which
          uses a TTW editable configuration, and for a pluggable configuration
          facility to inject contextual configuration settings as well.
        """
        context = aq_inner(self.context)
        view = getMultiAdapter((context, self.request),
                               name='pdfreactor-config')
        config = view()
        config.update({
            'document': self.converted_url(),
            })

        registry = getToolByName(context, 'portal_registry')
        proxy = registry.forInterface(IPdfReactorConnectionSettings)
        key = proxy.license_key or None
        if key is not None and key.strip().lower() != 'none':
            config['licenseKey'] = key
        return config

    def connectionSettings(self):
        """
        Return a {'headers': ..., 'cookies': ...} dict

        E.g. to create PDF documents from restricted contents,
        we need to provide cookies.

        For the basic backend configuration, see the make_reactor method.
        """
        request = self.request
        cookies = request.cookies
        return {
            'cookies': cookies,
            }

    def converted_url(self):
        """
        Return the URL to be fed to the PDFreactor service
        """
        return self.context.absolute_url()

    def __call__(self):
        """
        Send a request to the configured PDFreactor service, and return the PDF

        This is a simple solution for small exports which the user and her/his
        web browser is willing to wait for.
        For cases where browser timeouts are likely to occur, you should use
        asynchronous conversion.
        """
        pdfReactor = self.reactor
        config = self.conversionSettings()
        conn = self.connectionSettings()
        kw = {
            'config': config,
            'connectionSettings': conn,
            }
        result = pdfReactor.convertAsBinary(**kw)
        setHeader = self.request.response.setHeader
        setHeader("Content-type", "application/pdf")
        title = self.context.Title
        if callable(title):
            title = title()
        fname = title.strip()+'.pdf'
        setHeader('Content-Disposition', 'attachment; filename="%s"' % fname)
        return result
