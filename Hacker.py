"""
File: Hacker.py
Description: Defines the Rig class and related methods required for the Basic Programming Assignment.
Author: Erica Box
Author: Erica Box
ID: 110468687
Username: boxey001
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from Rig import Rig
from Asset import CryptoToken
from Asset import SecurityChip
from Asset import DataSpike


class Hacker:
    def __init__(self, name: str):
        self.name = name
        self.inventory = [CryptoToken("CryptoToken", "Used to acquire rigs.")]
        self.rig = None
        self.trace_level = 0

    def acquire_rig(self):
        self.inventory.remove(CryptoToken("CryptoToken", "Used to acquire rigs."))
        self.rig = Rig("Hail Mary")
        print("Rig acquired")

    def launch_data_spikes(self, target: Rig):
        # Ensure target is a Rig instance
        if not isinstance(target, Rig):
            print("Target is not a rig")
        # Consume a DataSpike instance
        for item in self.inventory:
            if isinstance(item, DataSpike):
                self.inventory.remove(item)
                target.take_hit()
        print("No DataSpike available.")


def encrypt_assets(self):
    chip_location = None
    chip = None

    # Check the Hacker's inventory for a SecurityChip
    for item in self.inventory:
        if isinstance(item, SecurityChip):
            chip = item
            chip_location = "inventory"
            break

    # If no chip was found in the Hacker's inventory, check the Hacker's rig - if they have one
    if chip is None and self.rig:
        for item in self.rig.storage:
            if isinstance(item, SecurityChip):
                chip = item
                chip_location = "rig"
                break

    if chip is None:
        print("Security chip needed to encrypt assets.")
        return
