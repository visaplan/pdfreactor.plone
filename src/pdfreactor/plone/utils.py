"""
pdfreactor.plone:utils: utilities
"""


def check_convert_kwargs(dic):
    """
    Check the keyword arguments for the .base.Exporter.convert method

    This function modifies the given kwargs dict in-place, checks them for
    sanity and injects missing keys, to allow for a pretty simple
    implementation of that method.

    For the doctests, we'll use a little helper function:
    >>> def cck(dic, copy=1):
    ...     if copy: dic=dict(dic)
    ...     check_convert_kwargs(dic)
    ...     dic['_given'] = sorted(dic['_given'])
    ...     return sorted(dic.items())

    By default, we'll return binary data:
    >>> cck({})  # doctest: +NORMALIZE_WHITESPACE
    [('_given',  []),
     ('as_json', False),
     ('async',   False),
     ('binary',  True),
     ('stream',  None)]
    >>> cck({'async': 1})  # doctest: +NORMALIZE_WHITESPACE
    [('_given',  ['async']),
     ('as_json', False),
     ('async',   1),
     ('binary',  False),
     ('stream',  None)]

    A stream argument is valid only for .convertAsBinary, so:
    >>> cck({'stream': '<some open file>'})  # doctest: +NORMALIZE_WHITESPACE
    [('_given',  ['stream']),
     ('as_json', False),
     ('async',   False),
     ('binary',  True),
     ('stream',  '<some open file>')]



    """
    _given = set(dic.keys())
    if '_given' in _given:
        raise TypeError('The _given argument is reserved!')
    dic['_given'] = _given
    if dic.setdefault('stream', None) is not None:
        binary = dic.setdefault('binary',  True)
        as_json = dic.setdefault('as_json', False)
        if binary is None:
            dic['binary'] = True  # freeze it
        elif not binary:
            raise TypeError('With a not-None stream (%s), '
                            'binary must be True!'
                            % (type(stream),
                               ))
        if as_json is None:
            dic['as_json'] = False  # freeze it
        elif as_json:
            raise TypeError('A not-None stream (%s) implies binary=True, and '
                            'as_json must be False!'
                            % (type(stream),
                               ))
        if dic.setdefault('async', False):
            raise TypeError("Currently, we don't support async together with "
                            'a given stream!')
            # ... we might do so, one day! 
    elif dic.setdefault('async', False):
        if dic.setdefault('binary', False):
            raise TypeError('binary conflicts with async; the latter returns '
                            'a documentId only, for later retrieval!')
        if dic.setdefault('as_json', False):
            raise TypeError('as_json conflicts with async; the latter returns '
                            'a documentId only, for later retrieval!')
    else:
        binary = dic.get('binary')
        as_json = dic.setdefault('as_json', False)
        if binary is None:
            dic['binary'] = not as_json
        elif as_json is None:
            dic['as_json'] = not binary
        elif as_json:
            if binary:
                raise TypeError('Both binary and as_json are True!')



if __name__ == '__main__':
    from doctest import testmod
    testmod()
