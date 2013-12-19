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
import re

def _wordlist(txt):
    return re.findall('\w+', txt.lower())

def _is_swearword(w):
    swearwordsrx = api.get('swearwords')
    word = w.lower()
    for sw in swearwordsrx:
        if re.match(sw, word):
            return True

    return False

# Append dictionary too the context
api.setdict({"swearwords":['fuck\w*', 'shit\w*'], 'nearby-word-distance': 3})

@api.advertise(mapping=False, domain="attribute-resolvers")
def nearby_swearwords(fetcher, article, attribute):
    """
    Get nearby swearwords from attribute. Check the context for a list
    of swearword regexps.
    """

    words = _wordlist(article)
    dist = api.get('nearby-word-distance')
    try:
        wl = words.index(attribute)
    except ValueError:
        return None

    # It is advised to use the configuration whenever possible
    return api.domaincall("static-attribute-resolvers", "swearwords",
                          words[max(0,wl-dist) : min(wl+dist, len(words))])


@api.advertise(domain="static-attribute-resolvers", name="swearwords")
def swearwords(article):
    """
    Get all article swearwords.
    """

    words = isinstance(article, str) and _wordlist(article) or article
    return filter(_is_swearword, words)


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
        if val is not None:
            return val
