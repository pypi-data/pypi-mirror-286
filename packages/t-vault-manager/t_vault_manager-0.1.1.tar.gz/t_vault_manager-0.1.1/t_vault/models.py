from abc import ABC, abstractmethod

import pyotp
from t_object import ThoughtfulObject

from t_vault.utils import exceptions


class Attachment(ThoughtfulObject):
    """A class representing an attachment with a name, item ID, and URL."""

    name: str
    item_id: str
    url: str


class VaultItem(ThoughtfulObject, ABC):
    """A class representing a vault item."""

    name: str = ""
    item_id: str = ""
    totp_key: str | None = None
    attachments: list[Attachment] = []
    fields: dict[str, str | None] = {}
    url_list: list[str] = []
    username: str | None = None
    password: str | None = None

    @abstractmethod
    def get_attachment(self, attachment_name: str) -> str:
        """Get an attachment by name.

        Args:
            attachment_name: The name of the attachment to retrieve.

        Returns:
            str: The path to the downloaded attachment.
        """
        raise NotImplementedError()

    @property
    def otp_now(self) -> str | None:
        """Returns the current TOTP code generated using the TOTP key associated with the instance.

        Returns:
            str: The current TOTP code, or None if no TOTP key is set.
        """
        return pyotp.TOTP(self.totp_key).now() if self.totp_key else None

    def __getitem__(self, key):
        """Get an item by key.

        Args:
            key: The key to retrieve the item.

        Returns:
            The item corresponding to the key, or the username if key is "login".
        """
        if key == "login":
            return self.username
        try:
            return self.fields[key]
        except KeyError:
            return getattr(self, key)


class BitWardenItem(VaultItem):
    """A class representing a Bitwarden vault item."""

    collection_id_list: list[str] = []
    folder_id: str | None = None
    notes: str | None = None

    def get_attachment(self, attachment_name: str) -> str:
        """Get an attachment by name.

        Args:
            attachment_name: The name of the attachment to retrieve.

        Returns:
            str: The path to the downloaded attachment.
        """
        attachment = next((attachment for attachment in self.attachments if attachment.name == attachment_name), None)
        if attachment is None:
            raise exceptions.VaultAttatchmentNotFoundError(f"Attachment '{attachment_name}' not found.")

        # TODO: Implement download functionality in bw class
        return ""
