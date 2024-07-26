"""
.. Lump 38 - Prim Verts

This lump contains an array of :any:`dprimvert_t`.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()

from construct import *  # NOQA: #402
from valvebsp.structs.common import *  # NOQA #402

dprimvert_t = Struct(
    'pos' / Vector
)


@lump_array
@lump_version(0)
def lump_38(header, profile=None):
    return dprimvert_t
