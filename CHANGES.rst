Changelog
=========


1.0.2 (2023-01-20)
------------------

New Features:

- For `MathML` support:
 
  - added a `@@pdfreactor-mathjax-vars.js` view (for configuration),
    and 
  - a ``++resource++pdfreactor.plone/mathjax2-run.js``
    script to ease MathJax integration.

  This is not configurable yet, but will likely be, soon.

- The @@as.pdf method supports a `method` option; e.g., call
  ``.../my/page/@@as.pdf?method=@@from-screeshot`` to create a PDF file from
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
