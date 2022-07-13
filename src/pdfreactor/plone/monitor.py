"""
@@pdf-monitor: target for PDFreactor callbacks

This BrowserView currently doesn't do anything very useful yet;
but you might use it as a hint how to build your own.

What you might want to do:

- for FINISH callbacks:
  - send a notification email, containing a download link
  - download the document from the PDFreactor service to your server

- for PROGRESS callbacks:
  - log about the progress

- for START callbacks:
  - log about the request being accepted,
  - or about possible configuration or server problems
"""

# Standard library:
from json import loads

# PDFreactor (by RealObjects; Python integration by visaplan GmbH):
from pdfreactor.api import PDFreactor

# Zope:
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.interface import implementer, implements
from zope.publisher.interfaces import IPublishTraverse

# Local imports:
from pdfreactor.plone.base import Exporter
from pdfreactor.plone.interfaces import (
    ICallbackMonitor,
    IPdfReactorConnectionSettings,
    )

# Logging / Debugging:
from logging import getLogger

logger = getLogger('@@pdf-monitor')

@implementer(IPublishTraverse)
class Monitor(Exporter):

    implements(ICallbackMonitor)

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.subpath = []

    def publishTraverse(self, request, name):
        self.subpath.append(name)
        return self

    def send_mail(self, to, data):
        """
        Send a notification mail
        (TODO; not implemented yet, since our mail current processing looks
        quite non-standard)
        """

    def __call__(self):
        """
        Receive notification callbacks by the PDFreactor service
        """
        context = self.context
        request = self.request

        subpath = self.subpath
        user_id = subpath.pop(0)
        uid = subpath.pop(0)
        o_pa = '/'.join(subpath)

        body = request.get('BODY')
        dic = loads(body)
        documentId = dic['documentId']

        acl = getToolByName(context, 'acl_users')
        user = acl.getUser(user_id)
        # ... get the mail address here, and send a mail ...

        logger.info('PDFreactor callback for UID %(uid)r by user %(user_id)s'
                    ' (path: %(o_pa)r)', locals())
        pdfReactor = self.reactor
        conn = self.connectionSettings()

        meta = pdfReactor.getDocumentMetadata(documentId, conn)
        # ... or .getDocumentAsBinary, or whatever you need

        # Just to make this browser view "testable" (half-way; when calling it
        # in your web browser, you won't have a POST body with JSON data).
        # In use as a callback target, nobody will ever bother about the
        # redirection; it will just be logged (and possibly course confusion),
        # so you'll normally remove it.
        request.response.redirect('/'+o_pa)
