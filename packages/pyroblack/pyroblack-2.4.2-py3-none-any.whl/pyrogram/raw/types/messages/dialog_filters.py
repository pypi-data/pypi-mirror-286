#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#  #  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#
#  This file is part of pyroblack.
#
#  pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with pyroblack.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class DialogFilters(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.messages.DialogFilters`.

    Details:
        - Layer: ``184``
        - ID: ``2AD93719``

    Parameters:
        filters (List of :obj:`DialogFilter <pyrogram.raw.base.DialogFilter>`):
            N/A

        tags_enabled (``bool``, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetDialogFilters
    """

    __slots__: List[str] = ["filters", "tags_enabled"]

    ID = 0x2ad93719
    QUALNAME = "types.messages.DialogFilters"

    def __init__(self, *, filters: List["raw.base.DialogFilter"], tags_enabled: Optional[bool] = None) -> None:
        self.filters = filters  # Vector<DialogFilter>
        self.tags_enabled = tags_enabled  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DialogFilters":
        
        flags = Int.read(b)
        
        tags_enabled = True if flags & (1 << 0) else False
        filters = TLObject.read(b)
        
        return DialogFilters(filters=filters, tags_enabled=tags_enabled)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.tags_enabled else 0
        b.write(Int(flags))
        
        b.write(Vector(self.filters))
        
        return b.getvalue()
