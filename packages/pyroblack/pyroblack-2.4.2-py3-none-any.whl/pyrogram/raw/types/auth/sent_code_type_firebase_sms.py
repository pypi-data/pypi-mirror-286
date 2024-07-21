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


class SentCodeTypeFirebaseSms(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.auth.SentCodeType`.

    Details:
        - Layer: ``184``
        - ID: ``9FD736``

    Parameters:
        length (``int`` ``32-bit``):
            N/A

        nonce (``bytes``, *optional*):
            N/A

        play_integrity_project_id (``int`` ``64-bit``, *optional*):
            N/A

        play_integrity_nonce (``bytes``, *optional*):
            N/A

        receipt (``str``, *optional*):
            N/A

        push_timeout (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["length", "nonce", "play_integrity_project_id", "play_integrity_nonce", "receipt", "push_timeout"]

    ID = 0x9fd736
    QUALNAME = "types.auth.SentCodeTypeFirebaseSms"

    def __init__(self, *, length: int, nonce: Optional[bytes] = None, play_integrity_project_id: Optional[int] = None, play_integrity_nonce: Optional[bytes] = None, receipt: Optional[str] = None, push_timeout: Optional[int] = None) -> None:
        self.length = length  # int
        self.nonce = nonce  # flags.0?bytes
        self.play_integrity_project_id = play_integrity_project_id  # flags.2?long
        self.play_integrity_nonce = play_integrity_nonce  # flags.2?bytes
        self.receipt = receipt  # flags.1?string
        self.push_timeout = push_timeout  # flags.1?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SentCodeTypeFirebaseSms":
        
        flags = Int.read(b)
        
        nonce = Bytes.read(b) if flags & (1 << 0) else None
        play_integrity_project_id = Long.read(b) if flags & (1 << 2) else None
        play_integrity_nonce = Bytes.read(b) if flags & (1 << 2) else None
        receipt = String.read(b) if flags & (1 << 1) else None
        push_timeout = Int.read(b) if flags & (1 << 1) else None
        length = Int.read(b)
        
        return SentCodeTypeFirebaseSms(length=length, nonce=nonce, play_integrity_project_id=play_integrity_project_id, play_integrity_nonce=play_integrity_nonce, receipt=receipt, push_timeout=push_timeout)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.nonce is not None else 0
        flags |= (1 << 2) if self.play_integrity_project_id is not None else 0
        flags |= (1 << 2) if self.play_integrity_nonce is not None else 0
        flags |= (1 << 1) if self.receipt is not None else 0
        flags |= (1 << 1) if self.push_timeout is not None else 0
        b.write(Int(flags))
        
        if self.nonce is not None:
            b.write(Bytes(self.nonce))
        
        if self.play_integrity_project_id is not None:
            b.write(Long(self.play_integrity_project_id))
        
        if self.play_integrity_nonce is not None:
            b.write(Bytes(self.play_integrity_nonce))
        
        if self.receipt is not None:
            b.write(String(self.receipt))
        
        if self.push_timeout is not None:
            b.write(Int(self.push_timeout))
        
        b.write(Int(self.length))
        
        return b.getvalue()
