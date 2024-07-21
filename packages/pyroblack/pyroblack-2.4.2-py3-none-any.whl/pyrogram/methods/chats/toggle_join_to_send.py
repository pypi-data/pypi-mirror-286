#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import errors


class ToggleJoinToSend:
    async def toggle_join_to_send(
        self: "pyrogram.Client", chat_id: Union[int, str], enabled: bool = False
    ) -> bool:
        """Enable or disable guest users' ability to send messages in a supergroup.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            enabled (``bool``):
                The new status. Pass True to enable guest users to send message.

        Returns:
            ``bool``: True on success. False otherwise.

        Example:
            .. code-block:: python

                # Change status of guests sending messages to disabled
                await app.toggle_join_to_send()

                # Change status of guests sending messages to enabled
                await app.toggle_join_to_send(enabled=True)
        """
        try:
            r = await self.invoke(
                raw.functions.channels.ToggleJoinToSend(
                    channel=await self.resolve_peer(chat_id), enabled=enabled
                )
            )

            return bool(r)
        except errors.RPCError:
            return False
