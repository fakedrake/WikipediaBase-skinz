from sexpdata import loads, dumps, Symbol, Quoted

import wikipediabase.api as api

def sexp_eval(ls):
    if hasattr(ls, "__iter__"):
        return api.call(*[sexp_eval(i) for i in ls])

    # We only know symbol functions as symbols
    if isinstance(ls, Symbol) or isinstance(ls, Quoted):
        return ls.value()
    else:
        return ls


@api.advertise(domain="frontend", append=False)
def text_frontend(inp):
    return sexp_eval(loads(inp))
