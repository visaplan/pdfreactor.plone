"""
@@request-pdf browser: request asynchronous PDF export

This is for more complex PDF exports which might take longer than a user agent
could be reasonably expected to wait for.

We don't provide the resulting document ourselves here but instead tell the
PDFreactor service to notify us, using the @@pdf-monitor view (./monitor.py).

NOTE:
- This is unfinished work, since the corresponding Monitor BrowserView
  is not fully implemented yet (./monitor.py);
  For this reason, both are not activated yet in ZCML code (./configure.zcml).
- Since both might become activated in a future version, you should be aware of
  possible future configuration conflicts and e.g. use a layer to make your
  implementation more specific than this one.

Most functionality can be inherited from our base Exporter class (./base.py).
"""

# Standard library (Python 2):
from urlparse import urlsplit, urlunsplit

# PDFreactor (by RealObjects; Python integration by visaplan GmbH):
from pdfreactor.api import PDFreactor

# Zope:
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.interface import implements

# Plone:
from plone.uuid.interfaces import IUUID

# 3rd party:
from urllib2 import quote

# Local imports:
from .base import Exporter
from pdfreactor.plone.interfaces import (
    IAsynchronousExporter,
    IPdfReactorConnectionSettings,
    )

# Logging / Debugging:
from logging import getLogger

logger = getLogger('@@request-pdf')


class AsynchronousExporter(Exporter):

    implements(IAsynchronousExporter)

    def __call__(self):
        """
        Send a request for asynchronous conversion to the PDFreactor service,
        and return the documentId.

        This is for more complex documents which would take too much time
        for a common user agent to wait.

        Instead of the naked docoumentId, you might want to return JSON data
        or redirect to a page, with a message injected.
        """
        context = self.context
        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            # we need to send an email, so we need a user:
            raise Unauthorized

        auth_member = pm.getAuthenticatedMember()
        userid = auth_member.getId()

        callback_url = context.absolute_url()
        parsed = urlsplit(callback_url)
        ulli = list(parsed)
        opa = ulli[2]
        # perhaps inject the callback action as well?
        # (but FINISH is really the most important; we get the documentId here
        # anyway, so START is not of too much interest, and PROGRESS
        # information is easiest presented to the user by getProgress requests)
        ulli[2] = ('/@@pdf-monitor/'
                   + quote(userid, safe='')
                   + '/'
                   + IUUID(context, None)
                   + opa)
        callback_url = urlunsplit(ulli)

        logger.info('Requesting PDF for %(context)r ...', locals())
        pdfReactor = self.reactor
        config = self.conversionSettings()
        config['callbacks'] = [{
            'contentType': PDFreactor.ContentType.JSON,
            'type': PDFreactor.CallbackType.FINISH,
            'url': callback_url,
        }]
        conn = self.connectionSettings()
        kw = {
            'config': config,
            'connectionSettings': conn,
            }
        documentId = pdfReactor.convertAsync(**kw)
        logger.info('PDF for %(context)r: documentId=%(documentId)r', locals())
