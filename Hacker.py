"""
File: Hacker.py
Description: Defines the Rig class and related methods required for the Basic Programming Assignment.
Author: Erica Box
ID: 110468687
Username: boxey001
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from Rig import Rig
from Asset import CryptoToken, SecurityChip, DataSpike, BaseAsset  # Added BaseAsset


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
                break
        self.rig = Rig("Hail Mary")
        print("Rig acquired")

    def launch_data_spikes(self, target: Rig):
        if not isinstance(target, Rig):
            print("Target is not a rig")
            return

        for item in self.inventory:
            if isinstance(item, DataSpike):
                self.inventory.remove(item)
                target.damage_counter += 1
                print("DataSpike launched")
                return
        print("No DataSpike available.")

    def remove_security_chip(self):
        if self.chip_location == "inventory":
            self.inventory.remove(self.chip)
            print("Security chip removed from inventory.")
        elif self.chip_location == "rig":
            self.rig.storage.remove(self.chip)
            print("Security chip removed from storage.")

    def encrypt_assets(self):
        """Search for a SecurityChip and encrypt assets in inventory and rig storage."""
        self.inventory_encrypted = False
        self.rig_storage_encrypted = False
        self.chip = None
        self.chip_location = None

        # Search inventory for chip
        for item in self.inventory:
            if isinstance(item, SecurityChip):
                self.chip = item
                self.chip_location = "inventory"
                break

        # Search rig storage if not found in inventory
        if self.chip is None and self.rig:
            for item in self.rig.storage:
                if isinstance(item, SecurityChip):
                    self.chip = item
                    self.chip_location = "rig"
                    break

        if self.chip is None:
            print("Security chip needed to encrypt assets.")
            return

        for item in self.inventory:
            if not item.encrypted:
                item.encrypted = True
                self.inventory_encrypted = True

        if self.rig:
            for item in self.rig.storage:
                if not item.encrypted:
                    item.encrypted = True
                    self.rig_storage_encrypted = True

        if self.inventory_encrypted and self.rig_storage_encrypted:
            print("Assets from inventory and rig's storage have been encrypted.")
            self.remove_security_chip()
        elif self.inventory_encrypted:
            print("Assets from inventory have been encrypted.")
            self.remove_security_chip()
        else:
            print("No assets have been encrypted.")

    def decrypt_target_rig(self, target: "Rig"):
        """
        Decrypt assets in a target Rig, if it is broken and a SecurityChip is available.
        """
        if not isinstance(target, Rig):
            print("Target is not a valid Rig.")
            return
        if not target.broken_state:
            print(f"Cannot decrypt {target.name}: target rig is not broken/exposed.")
            return

        # Reset chip
        self.chip = None
        self.chip_location = None

        # Search inventory for chip
        for item in self.inventory:
            if isinstance(item, SecurityChip):
                self.chip = item
                self.chip_location = "inventory"
                break

        # If not found, search rig storage
        if self.chip is None and self.rig:
            for item in self.rig.storage:
                if isinstance(item, SecurityChip):
                    self.chip = item
                    self.chip_location = "rig"
                    break

        if self.chip is None:
            print("Security Chip needed to decrypt target rig assets.")
            return

        # Attempt to decrypt assets
        decrypted_any = False
        for asset in target.storage:
            if isinstance(asset, BaseAsset) and asset.encrypted:
                asset.encrypted = False
                decrypted_any = True
                print(f"{asset.name} in {target.name} decrypted.")

        if decrypted_any:
            if self.chip_location == "inventory" and self.chip in self.inventory:
                self.inventory.remove(self.chip)
            elif self.chip_location == "rig" and self.chip in self.rig.storage:
                self.rig.storage.remove(self.chip)
            print("Target assets have been decrypted successfully.")
        else:
            print("Assets are already decrypted. SecurityChip not consumed.")
