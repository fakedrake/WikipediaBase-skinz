import api

@api.advertise(domain="static-attribute-resolvers", name="yomama")
def yomama(attr):
    return "yomama "+attr

@api.advertise(mapping=False, domain="attribute-resolvers")
def named_resolvers(fetcher, article, attribute):
    resolvers = api.get("static-attribute-resolvers", function=True)

    return resolvers[attribute](article)

@api.advertise(domain="attribute-resolver", append=False)
def resolve_attribute(article, attr):
    resolvers = api.get("attribute-resolvers", function=True)
    for r in resolvers:
        val = r(None, article, attr)
        if val:
            return val
