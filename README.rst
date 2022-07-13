.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

================
pdfreactor.plone
================

This Add-On package integrates the PDFreactor_ client API by RealObjects_,
as provided by the pdfreactor-api_ package, into Plone.

To effectively make use of it, you'll need

- a running *PDFreactor* server
- the keys needed to access it;
  depending on the server configuration:

  - the license key (from *RealObjects*; see https://www.pdfreactor.com/buy/)
    (unless installed on the server)

    and
  - an API key, if required by the server.


Features
========

- A simple ``@@as.pdf`` browser view for contentish objects
  (providing a synchronous PDF export with standard options)
- A custom form ``@@pdfreactor-connection-settings`` to edit the
  *connection* settings (which are stored in the Plone registry)
- A simple ``@@pdfreactor-config`` view to provide basic *conversion* settings
  (i.e., the Zope cookies which are needed to create PDF exports from
  restricted contents)

  For a package providing customizable conversion settings in the registry as
  well, see below.

- A simple CSS stylesheet which is used by the default configuration to
  suppress uninteresting page parts


Installation
============

Plone environments are typically built using `zc.buildout`_;
so add to your ``buildout.cfg`` script::

    [buildout]
    ...
    eggs =
        pdfreactor.plone

and then run ``bin/buildout``.

This will get you the pdfreactor-api_ package as well.

After restarting your Zope instance, you'll find the package in
the Quick-Installer or
the Plone Add-Ons view.

After installing (or *activating*) the package there, go to the Plone registry
to customize your PDFreactor connection settings
(URL and license and / or API key);
look for the interface (or *prefix*) "IPdfReactorConnectionSettings".

For installation instructions regarding the PDFreactor service itself, please
refer to `PDFreactor Support`_.


Customization
=============

Zope / Plone
------------

You have several options:

- You may subclass our .base.Exporter BrowserView class
  (which provides the ``@@as.pdf`` view)
  and override some of it's methods,
  e.g.

  - converted_url
  - conversionSettings

- You may connect our BrowserView class or subclasses of it
  to more specific interfaces than IContentish.
  (You might need a layer interface to avoid configuration conflicts).

- You may override the ``@@pdfreactor-config`` view to modify the conversion
  options (generally, or by interface).

  One add-on package to get a global "TTW" customizable configuration is
  pdfreactor.parsecfg_.

Please refer to the Zope / Plone documentation for instructions how to do this.


PDFreactor
----------

For the details about the supported methods and configuration options of the
*PDFreactor* itself,
please refer to the documentation by *RealObjects GmbH*:

- `PDFreactor Web service documentation`_


Support
=======

If you are having issues *concerning this Plone integration*,
please let us know;
please use the `issue tracker`_ mentioned above.

For issues regarding the *PDFreactor* itself, please refer to *RealObjects GmbH*:

- `PDFreactor Support Center`_


Contribute
==========

(To this Plone integration package:)

- Issue Tracker: https://github.com/visaplan/pdfreactor.plone/issues
- Source Code: https://github.com/visaplan/pdfreactor.plone


License
=======

The project is licensed under the MIT License.

.. _`issue tracker`: https://github.com/visaplan/pdfreactor.plone/issues
.. _pdfreactor-api: https://pypi.org/project/pdfreactor-api
.. _pdfreactor.parsecfg: https://pypi.org/project/pdfreactor.parsecfg
.. _PDFreactor: https://www.pdfreactor.com
.. _PDFreactor Support Center: https://www.pdfreactor.com/support/
.. _PDFreactor Support: https://www.pdfreactor.com/support/
.. _PDFreactor Web service documentation: https://www.pdfreactor.com/product/doc/webservice/
.. _RealObjects: https://www.realobjects.com/
.. _zc.buildout: https://pypi.org/project/zc.buildout

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
