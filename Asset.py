"""
File: Asset.py
Description: <A brief description of this Python module.>
Author: <full name>
ID: <student_id>
Username: <username>
This is my own work as defined by the University's Academic Misconduct Policy.
"""


class BaseAsset:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.encrypted = False

    def __str__(self):
        if self.encrypted:
            return f'{self.name}: {self.description} [encrypted]'
        else:
            return f'{self.name}: {self.description}'


class CryptoToken(BaseAsset):
    pass


class DataSpike(BaseAsset):
    pass


class RemovableDrive(BaseAsset):
    pass


class SecurityChip(BaseAsset):
    pass


class HardwarePatch(BaseAsset):
    pass
