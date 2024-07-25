from tdqm import tqdm
from functools import partial

progressbar = partial(tqdm, leave=False)
# We put this here as we may also want to log some of these results...
