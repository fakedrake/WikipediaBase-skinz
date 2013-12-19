"""
A couple of token attribute resolvers. These are meant to be an
example on how to use resolvers yourself.

The function in the 'attribute-resolver' domain should run each
function in the 'attribute-resolvers' function list. Then each
attribute resolver may have it's own depository of functions in the
Context like a dictionary of functions in the domain
'static-attribute-resolvers'.
"""


import api

@api.advertise(domain="static-attribute-resolvers", name="yomama")
def yomama(article):
    """
    Just say "yomama" and then the article.
    """

    return "yomama " + article

@api.advertise(mapping=False, domain="attribute-resolvers")
def static_resolvers(fetcher, article, attribute):
    """
    Read from function dictionary 'static-attribute-resolvers' and call the
    one correspinding to the specific attribute.
    """

    resolvers = api.get("static-attribute-resolvers", function=True)

    if attribute in resolvers:
        resolver = resolvers[attribute]
        return resolver(article)
    else:
        return None

@api.advertise(domain="attribute-resolver", append=False)
def resolve_attribute(article, attr):
    """
    Look into 'attribute-resolvers' list of functions and return the
    first actual result.
    """

    resolvers = api.get("attribute-resolvers", function=True)
    for r in resolvers:
        val = r(None, article, attr)
        if val:
            return val
