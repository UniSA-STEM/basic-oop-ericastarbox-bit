"""
File: Rig.py
Description: Defines the Rig class
Author: Erica Box
ID: 110468687
Username: boxey001
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from Asset import DataSpike
from Asset import RemovableDrive


class Rig:
    def __init__(self, name: str):
        self.name = name
        self.damage_counter = 0
        self.broken_state = False
        self.storage = [DataSpike("DataSpike", "Used to encrypt and decrypt assets."),
                        DataSpike("DataSpike", "Used to encrypt and decrypt assets."),
                        RemovableDrive("RemovableDrive", "Used in battles.")]
        self.upgrade_level = 0
        self.rig_storage_encrypted = False
