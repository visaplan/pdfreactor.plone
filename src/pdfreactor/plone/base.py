"""
@@as.pdf browser: simple PDF export
"""
from urllib import urlencode
from urlparse import parse_qs, urlsplit
from urlparse import urlunsplit

# PDFreactor (by RealObjects; Python integration by visaplan GmbH):
from pdfreactor.api import PDFreactor

# Zope:
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.interface import implements

try:
    # Zope:
    from Globals import DevelopmentMode
except ImportError:
    # Hotfix for Zope 4; how to properly replace this?
    DevelopmentMode = False

import pkg_resources
try:
    pkg_resources.get_distribution('pdfreactor.parsecfg')
except pkg_resources.DistributionNotFound:
    HAVE_PARSECFG = 0
else:
    from pdfreactor.parsecfg.parse import generate_statements
    from pdfreactor.parsecfg.oldmethods import convert_api_method
    HAVE_PARSECFG = 1

try:
    pkg_resources.get_distribution('visaplan.tools')
except pkg_resources.DistributionNotFound:
    HAVE_VTOOLS = 0
else:
    from visaplan.tools.debug import pp
    HAVE_VTOOLS = 1

# Local imports:
from pdfreactor.plone.interfaces import (
    IExporter,
    IPdfReactorConnectionSettings,
    )
from ._mixin import GimmeCookies
from .utils import check_convert_kwargs


class Exporter(BrowserView, GimmeCookies):

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

        If you decide to override this method and not use @@pdfreactor-config,
        you'll most likely need to inject the Zope cookies in another way,
        e.g calling the getZopeCookies method yourself.
        """
        context = aq_inner(self.context)
        view = getMultiAdapter((context, self.request),
                               name='pdfreactor-config')
        config = view()
        config.update(self.conversionSource())

        registry = getToolByName(context, 'portal_registry')
        proxy = registry.forInterface(IPdfReactorConnectionSettings)
        key = proxy.license_key or None
        if key is not None and key.strip().lower() != 'none':
            config['licenseKey'] = key
        return config

    def allow_debug_mode(self, config):
        """
        Do we allow debug mode to be activated?

        Here we do so simply for (Zope2) instances with DevelopmentMode
        enabled; this might need to be more elaborated, though.
        """
        return DevelopmentMode

    def debug_mode(self, config):
        """
        If debugging output is requested,
        and if not prohibited (as of the .allow_debug_mode method),
        modify the given conversion settings dict in-place
        and return the truish form data.
        """
        form = self.request.form
        debug = form.get('debug', 0)
        if not debug:
            return False
        elif not self.allow_debug_mode(config):
            return False
        if HAVE_PARSECFG and 0:
            # Currently, this would only give us appendLogs=True;
            # we want more!
            # We might make this configurable in a future pdfreactor.parsecfg
            # release.
            stmt = list(generate_statements('enableDebugMode()'))[0]
            convert_api_method(stmt, config, {})
        else:
            dbg = config.setdefault('debugSettings', {})
            # for serious problems, 'appendLogs' probably won't be enough.
            dbg['all'] = True
        return {'debug': debug}

    def connectionSettings(self):
        """
        Override this method to inject a connectionSettings option

        Currently we don't really use connection settings as the PDFreactor API
        understands them:

        - the apiKey is attached to the reactor object,
        - the Zope cookies go in the 'cookies' key of the config option
          (see @@pdfreactor-config or the getZopeCookies method),
          and
        - the license key (unless installed on the PDFreactor server, as
          recommended) is considered 'config' as well.

        So, this method simply returns None; you might want to override it,
        e.g. to inject a dictionary to be updated from the server's answer,
        for repeated requests.

        We might need to support options for this to work; but since options
        are difficult to un-support, once the have been introduced, we don't
        support any for now.
        """
        return None  # pep 20.2

    def converted_url(self):
        """
        Return the URL to be fed to the PDFreactor service

        This method *consumes* the 'method' query option, if given.
        """
        base = self.context.absolute_url()
        method = self.request.form.pop('method', None)
        if not method:
            return base
        if not method.startswith('/'):
            method = '/' + method
        return base + method

    def conversionSource(self):
        """
        Return a dict providing the 'document' "configuration" string

        This may be a URL (like returned by .converted_url, above),
        or an [X]HTML or XML text.

        By default, we return a URL; override this method to use some
        ready-to-use text
        (which frees the PDFreactor service from the need to query your server).
        """
        return {'document': self.converted_url()}

    def convert(self, **kwargs):
        """
        Convert the context*; the return value type depends on the given args.
        All options must be given by name.

        Allowed options:

        as_json -- If true, binary must be (and defaults to) false (see below).
                   Implies the .convert API method.

                   Despite the name, we don't return a JSON string (which is
                   what the PDFreactor service returns to us)
                   but a Python dict which contains all available data.

        stream -- if given, we'll use it and write to that stream;
                  this implies "binary" output
                  and the use of the PDFreactor API method convertAsBinary.
                  
                  The return value will be None.

        async -- Call the convertAsync API method,
                 and return the documentId (a string),
                 as returned by the convertAsync API method.

                 You'll need to get the document yourself, e.g. by calling
                 getDocumentAsBinary.

        binary -- May be combined with a stream option, and implies
                  convertAsBinary.

                  Unless a stream is given, the binary data of the created PDF
                  document (or image, if the raster image extension is used)
                  is returned.

        config -- If not given, we'll call our conversionSource method;
                  this should return a dict with a 'document' key.

        connectionSettings --
                  If not given, we'll call our connectionSettings method

        document -- If the config value (see above) doesn't contain a
                    'document' key, you may specify that "document" (or image)
                    source yourself.

        """
        check_convert_kwargs(kwargs)
        GIVEN = kwargs['_given']
        config = (
                kwargs['config'] if 'config' in GIVEN
                else self.conversionSettings())
        connectionSettings = (
                kwargs['connectionSettings'] if 'connectionSettings' in GIVEN
                else self.connectionSettings())
        # we currently don't perform any sanity checks here ...
        # We don't expect any working conversion without a 'document' spec,
        # though. 
        if 'document' in GIVEN:
            if config is None:
                config = {}
            config['document'] = kwargs['document']

        ckw = {  # conversion keyword arguments
            'config': config,
            'connectionSettings': connectionSettings,
            }
        stream = kwargs['stream']
        if stream is not None:
            ckw['stream'] = stream

        # now for the conversion.
        reactor = self.reactor
        if kwargs['binary']:
            res = reactor.convertAsBinary(**ckw)
            if stream is not None:
                # a stream was specified and written to: 
                return None
            return res

        # the following won't take a stream argument;
        # but that's subject to our check_convert_kwargs function:
        elif kwargs['async']:
            doc_id = reactor.convertAsync(**ckw)
            return doc_id
        elif kwargs['as_json']:
            dic = reactor.convert(**ckw)
            return dic
        else:
            raise TypeError('Not binary nor async nor as_json?! '
                "We'd expect this to be handled "
                'by the check_convert_kwargs function!')

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
        dic = self.debug_mode(config)
        if dic:
            if HAVE_VTOOLS:
                pp(config=config, dic=dic)
            parsed = list(urlsplit(config['document']))
            qs = parsed[3]
            if qs:
                query = parse_qs(qs)
                query.update(dic)
            else:
                query = dic
            qs = urlencode(query)
            parsed[3] = qs
            config['document'] = urlunsplit(parsed)
            if HAVE_VTOOLS:
                pp(kw=kw)

        result = pdfReactor.convertAsBinary(**kw)
        setHeader = self.request.response.setHeader
        setHeader("Content-type", "application/pdf")
        title = self.context.Title
        if callable(title):
            title = title()
        fname = title.strip()+'.pdf'
        setHeader('Content-Disposition', 'attachment; filename="%s"' % fname)
        return result
