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

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputPrivacyRule = Union[raw.types.InputPrivacyValueAllowAll, raw.types.InputPrivacyValueAllowChatParticipants, raw.types.InputPrivacyValueAllowCloseFriends, raw.types.InputPrivacyValueAllowContacts, raw.types.InputPrivacyValueAllowPremium, raw.types.InputPrivacyValueAllowUsers, raw.types.InputPrivacyValueDisallowAll, raw.types.InputPrivacyValueDisallowChatParticipants, raw.types.InputPrivacyValueDisallowContacts, raw.types.InputPrivacyValueDisallowUsers]


# noinspection PyRedeclaration
class InputPrivacyRule:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 10 constructors available.

        .. currentmodule:: pyrogram.raw.types

        .. autosummary::
            :nosignatures:

            InputPrivacyValueAllowAll
            InputPrivacyValueAllowChatParticipants
            InputPrivacyValueAllowCloseFriends
            InputPrivacyValueAllowContacts
            InputPrivacyValueAllowPremium
            InputPrivacyValueAllowUsers
            InputPrivacyValueDisallowAll
            InputPrivacyValueDisallowChatParticipants
            InputPrivacyValueDisallowContacts
            InputPrivacyValueDisallowUsers
    """

    QUALNAME = "pyrogram.raw.base.InputPrivacyRule"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://eyMarv.github.io/pyroblack-docs/telegram/base/input-privacy-rule")
