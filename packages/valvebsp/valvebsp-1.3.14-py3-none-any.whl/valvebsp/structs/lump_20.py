"""
.. Lump 20 - Areas

This lump contains an array of :any:`darea_t`.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()

from construct import *  # NOQA: #402
from valvebsp.structs.common import *  # NOQA: #402

darea_t = Struct(
    'numAreaPortals' / Int32sl,
    'firstAreaPortal' / Int32sl * "index into :ref:`lump 21<lump_21>`"
)


@lump_array
@lump_version(0)
def lump_20(header, profile=None):
    return darea_t
