"""
Advertising means registering a function to the 'functions'
domain. From a user's standpoint in that domain lives a dictionary of
'name' -> *fn-obj* that is used by the front end to provide functions.
"""

from context import Context
from default import DEFAULTS_DOMAIN
from functions import MetaAdvert
from skin import Skin, DictSkinConfig

import types

def set(domain, value, function=False):
    Context.get_skin(function=function)[domain] = value


def get(domain, function=False, **kwargs):
    """
    Get a single piece of data. function needs to be true if you want
    a callable.
    """

    return Context.get_skin(function=function).get(domain, **kwargs)

def append(domain, value, function=False, **kwargs):
    return Context.get_skin(function=function).append(domain, value, **kwargs)

def defaults_decorator(fn):
    """
    Decorated function will have default args what is in
    DEFAULTS_DOMAIN of the context.
    """

    def wrap(*args, **kwargs):
        # Convert all positional arguments to kwargs
        argdic = dict(zip(fn.__code__.co_varnames, args))
        kw = (Context.get_skin(function=False).get(DEFAULTS_DOMAIN) or {}).copy()
        kw.update(kwargs)
        kw.update(argdic)

        return fn(**kw)

    return wrap

@defaults_decorator
def get_fn(name, domain=None, **kw):
    """
    Access functions in a domain.
    """

    d = Context.get_skin(function=True)[domain or name]
    try:
        return d[name]
    except TypeError:
        return d

def setdict(dic):
    """
    Creates a new skin with config dict.
    """

    Context.set_skin(Skin(DictSkinConfig(dic)))

def domaincall(domain, name, *args, **kwargs):
    return get_fn(name, domain=domain)(*args, **kwargs)

def freecall(name, *args, **kwargs):
    """
    Call a function saved in a 'name' domain.
    """

    return get_fn(name, domain=None)(*args, **kwargs)


def call(name, *args, **kwargs):
    """
    Call a function from the 'functions' domain.
    """

    return get_fn(name)(*args, **kwargs)

@defaults_decorator
def advertise_fn(func, **kwargs):
    Context.register_function(func, **kwargs)
    return func

@defaults_decorator
def advertise(name=None, domain=None, append=None, **kw):
    """
    To decorate methods of a class it needs to subclass
    `Advertisable`. Also this decorator implies `@staticmethod`.

    Decorator for advertising functions using their name as key, or
    provide a name and you may decorate with parameters. Default
    parameters are in DEFAULT_DOMAIN of context. You may see what
    params you can pass by looking at `Contex.register_function`.

    Provide domain and not name to put the vanilla function in the
    slot.
    """

    def real_dec(fn): return advertise_fn(fn, name=name,
                                          domain=domain,
                                          append=append, **kw)
    return real_dec

def jsondump():
    return Context.get_skin(function=False).dump()


def attribute_resolvers():
    """
    Get a list of the attribute resolvers available.
    """

    Context.get_skin(function=True)["resolvers"]


class Advertisable(object):
    """
    Subclassing this will give make your methods advertisable.
    """

    __metaclass__ = MetaAdvert
