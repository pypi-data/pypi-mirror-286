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


class SecureValueError(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.SecureValueError`.

    Details:
        - Layer: ``184``
        - ID: ``869D758F``

    Parameters:
        type (:obj:`SecureValueType <pyrogram.raw.base.SecureValueType>`):
            N/A

        hash (``bytes``):
            N/A

        text (``str``):
            N/A

    """

    __slots__: List[str] = ["type", "hash", "text"]

    ID = 0x869d758f
    QUALNAME = "types.SecureValueError"

    def __init__(self, *, type: "raw.base.SecureValueType", hash: bytes, text: str) -> None:
        self.type = type  # SecureValueType
        self.hash = hash  # bytes
        self.text = text  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SecureValueError":
        # No flags
        
        type = TLObject.read(b)
        
        hash = Bytes.read(b)
        
        text = String.read(b)
        
        return SecureValueError(type=type, hash=hash, text=text)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.type.write())
        
        b.write(Bytes(self.hash))
        
        b.write(String(self.text))
        
        return b.getvalue()
