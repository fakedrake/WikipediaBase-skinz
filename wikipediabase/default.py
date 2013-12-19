from context import Context
from skin import Skin, DictSkinConfig

DEFAULTS_DOMAIN = 'default_kwargs'
# Note that append as None means the user has not set the behaviour
# explicitly. It should be interpreted to true by the Context.
DEFAULTS_KW = dict(domain='functions', append=None, mapping=True)
DEFAULTS = DictSkinConfig(functions={}, default_kwargs=DEFAULTS_KW)

if Context._skin == None:
    Context.set_skin(Skin(config=DEFAULTS))
