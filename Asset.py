"""
File: Asset.py
Description: Defines the core assets required for the Basic Programming Assignment
Author: Erica Box
ID: 110468687
Username: boxey001
This is my own work as defined by the University's Academic Misconduct Policy.
"""


class BaseAsset:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._encrypted = False

    def __str__(self):
        encryption_status = " [encrypted]" if self._encrypted else ""
        return f'{self.name}: {self.description}{encryption_status}'


class CryptoToken(BaseAsset):
    def __init__(self):
        super().__init__("CryptoToken", "Used to acquire or repair rigs.")


class DataSpike(BaseAsset):
    def __init__(self):
        super().__init__("DataSpike", "Used in battles to damage enemy rigs.")


class RemovableDrive(BaseAsset):
    def __init__(self):
        super().__init__("RemovableDrive", "Used to extract unsecured assets.")


class SecurityChip(BaseAsset):
    def __init__(self):
        super().__init__("SecurityChip", "Used to encrypt or decrypt assets.")


class HardwarePatch(BaseAsset):
    def __init__(self):
        super().__init__("HardwarePatch", "Used to upgrade rigs.")


# ---------- Properties ----------
@property
def encrypted(self):
    """
    Get encryption status.
    """
    return self._encrypted


@encrypted.setter
def encrypted(self, value: bool):
    """
    Set encryption status.
    """
    self._encrypted = value
