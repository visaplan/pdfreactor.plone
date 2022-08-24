Changelog
=========


1.0.1 (unreleased)
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
