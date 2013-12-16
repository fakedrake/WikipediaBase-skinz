import importlib

from wikipediabase.skin import Skin

class FunctionSkin(Skin):
    """
    A dict-like container and interface for wikipediabase
    functions. Functions are stored in the form of (module_name,
    function_name)
    """

    def __init__(self, functions = [], *args, **kwargs):
        """
        Initialize yourself using a dict-like list of funtions.
        """

        super(FunctionSkin, self).__init__(*args, **kwargs)

        self.set('functions', functions)

    def call(self, name, *args, **kwargs):
        """
        Call function given by name wnith arguments.
        """

        mn, fn = self[name]
        m = importlib.import_module(mn)
        f = getattr(m, fn)

        return f(*args, **kwargs)


    def add_function(self, fn, name=None):
        self[name or fn.__name__] = (fn.__module__, fn.__name__)
