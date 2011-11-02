Changelog
=========


v0.2.1
--------

Major bugfix release

- Fixed an issue with the caching that prevented it from being used.


v0.2.0
--------

Major imporovements to the app and the test suite. Some of these are:

- Refactored the API. URLMiddleware is now imported with the shorter
  'urlmiddleware.URLMiddleware' rather than 'urlmiddleware.middlware.URLMiddleware'

- Make sure that middleware is only called once, even when added twice with
  the same url pattern.

- Add memoizing to the pattern matching to improve performance.

- A vastly improved test suite that offers good coverage of the code.

- Initial draft of basic documentation.
