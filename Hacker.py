"""
File: Hacker.py
Description: Defines the Rig class and related methods required for the Basic Programming Assignment.
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
        self.chip_location = None
        self.chip = None
        self.inventory_encrypted = False
        self.rig_storage_encrypted = False

    def acquire_rig(self):
        for item in self.inventory:
            if isinstance(item, CryptoToken):
                self.inventory.remove(item)
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
                target.damage_counter += 1
                print("DataSpike launched")
                return
        print("No DataSpike available.")

    def remove_security_chip(self):
        # Checks for location of SecurityChip instance and removes it.
        if self.chip_location == "inventory":
            self.inventory.remove(self.chip)
            print("Security chip removed from inventory.")
        elif self.chip_location == "rig":
            self.rig.storage.remove(self.chip)
            print("Security chip removed from storage.")

    def encrypt_assets(self):
        # Reset instance variables at the beginning of encrypt assets to clear any previous encryption efforts
        self.inventory_encrypted: False
        self.rig_storage_encrypted: False
        # Check the Hacker's inventory for a SecurityChip
        for item in self.inventory:
            if isinstance(item, SecurityChip):
                self.chip = item
                self.chip_location = "inventory"
                break

        # If no chip was found in the Hacker's inventory, check the Hacker's rig - if they have one
        if self.chip is None and self.rig:
            if self.rig:
                for item in self.rig.storage:
                    if isinstance(item, SecurityChip):
                        self.chip = item
                        self.chip_location = "rig"
                        break

        # If no chip was found, end method and advise that a Security Chip is needed to encrypt assets.
        if self.chip is None:
            print("Security chip needed to encrypt assets.")
            return

        for item in self.inventory:
            if not item.encrypted:
                item.encrypted = True
                self.inventory_encrypted = True

        for item in self.rig.storage:
            if not item.encrypted:
                item.encrypted = True
                self.rig_storage_encrypted = True

        if self.inventory_encrypted and self.rig_storage_encrypted:
            print("Assets from inventory and rig's storage have been encrypted.")
            self.remove_security_chip()
        elif self.inventory_encrypted and not self.rig_storage_encrypted:
            print("Assets from inventory have been encrypted.")
            self.remove_security_chip()
        elif not self.inventory_encrypted and not self.rig_storage_encrypted:
            print("No assets have been encrypted.")
