Changelog
=========


1.0.3 (2023-04-05)
------------------

New Features:

- The .base.Exporter class now provides an own `.convert` method
  which accepts `binary`, `async` and `stream` arguments
  and calls the appropriate conversion method internally.

  Currently, it will return

  - `None`, if a `stream` was given,
  - binary data, if `binary` was given (and not `stream`), and
  - the document_id, if `async` was given, and
  - a `dict` with all meta information contained otherwise.

Improvements:

- The .base.Exporter class now provides (and uses) a `conversionSource`
  method which in turn uses the existing `converted_url` method.

  **Note:** if providing text instead of a URL as the ``document`` config key,
  you likely need to specify a ``baseUrl`` as well; otherwise the reactor
  might fail to load stylesheets or images during conversion.

Development hints:

- When developing and testing your PDFreactor_ conversions,
  be sure you have more than one Zope worker thread ready;
  otherwise you might wonder about HTTP errors
  when the reactor sends requests to your instance!

- We provide the original API (from the PDFreactor_ distribution) as `.raw_api`
  module (for development and testing;
  helps to check whether a certain problem
  is related to our pythonization measures).

  Just in case.

[tobiasherp]


1.0.2 (2023-01-20)
------------------

New Features:

- For `MathML` support:
 
  - added a `@@pdfreactor-mathjax-vars.js` view (for configuration),
    and 
  - a ``++resource++pdfreactor.plone/mathjax2-run.js``
    script to ease MathJax_ integration.

  This is not configurable yet, but will likely be, soon.

  **Note:** `PDFreactor v11.6.3`_ (2023-03-07) contains a fix
  to a bug which caused `MathML` exports as "continuous media" to fail.

- The @@as.pdf method supports a `method` option; e.g., call
  ``.../my/page/@@as.pdf?method=@@from-screenshot`` to create a PDF file from
  ``.../my/page/@@from-screenshot``.

[tobiasherp]


1.0.1 (2022-09-20)
------------------

Miscellaneous:

- The `connectionSettings` method doesn't return any cookies anymore
  because the Zope cookies are considered `config` information.
- The .base.Exporter provides a `getZopeCookies` method now
  for use in derived view classes which override the `conversionSettings`
  method to not use @@pdfreactor-config.

[tobiasherp]


1.0.0 (2022-07-12)
------------------

- Initial release.
  [tobiasherp]

.. _MathJax: https://www.mathjax.org
.. _PDFreactor: https://www.pdfreactor.com
.. _`PDFreactor v11.6.3`: https://www.pdfreactor.com/product/changelog.htm#v11.6.3
