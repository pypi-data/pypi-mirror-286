# -*- coding: utf-8 -*-
from .asset.asset import OxaigenAsset
from .authentication.authentication import OxaigenAuthentication
from .storage.data_storage import OxaigenDataStorage


class Oxaigen:
    """
    Oxaigen SDK Class
    """

    def __init__(self):
        self.auth = OxaigenAuthentication()
        self.asset = OxaigenAsset()
        self.storage = OxaigenDataStorage()

    def login(self):
        """
        Interactive function to log in.

        This function prompts the user for a username and password
        (hidden for security reasons). It then authenticates the user
        and generates a token, saving it to a `token.json` file in the
        `.oxaigen` directory in the user's home directory.

        Returns:
            None
        """
        self.auth.login()
