"""
File: Hacker.py
Description: Defines the Hacker class and related methods required for the Basic Programming Assignment.
Author: Erica Box
ID: 110468687
Username: boxey001
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from Rig import Rig
from Asset import CryptoToken, SecurityChip, DataSpike, BaseAsset, HardwarePatch


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

    # ---------- Helper Methods ----------

    def find_and_remove_from_inventory(self, item_type):
        """Find and remove the first instance of the specified type in the Hacker's inventory."""
        for item in self.inventory:
            if isinstance(item, item_type):
                self.inventory.remove(item)
                return item
        return None

    def find_item_type(self, item_class: type):
        """Search for BaseAsset instance type in the inventory or rig storage."""
        for item in self.inventory:
            if isinstance(item, item_class):
                return item, "inventory"
        if self.rig:
            for item in self.rig.storage:
                if isinstance(item, item_class):
                    return item, "rig"
        return None

    def encrypt_items(self, items):
        """Encrypts all unencrypted items in a list. Returns True if any were encrypted."""
        encrypted_any = False
        for item in items:
            if not item.encrypted:
                item.encrypted = True
                encrypted_any = True
        return encrypted_any

    def decrypt_items(self, items):
        """Decrypt all encrypted items in a list. Return True if any were decrypted."""
        decrypted_any = False
        for item in items:
            if isinstance(item, BaseAsset) and item.encrypted:
                item.encrypted = False
                decrypted_any = True
                print(f"{item.name} decrypted.")
        return decrypted_any

    def remove_security_chip(self):
        """Remove the current SecurityChip from its location (inventory or rig)."""
        if self.chip_location == "inventory" and self.chip in self.inventory:
            self.inventory.remove(self.chip)
            print("Security chip removed from inventory.")
        elif self.chip_location == "rig" and self.rig and self.chip in self.rig.storage:
            self.rig.storage.remove(self.chip)
            print("Security chip removed from rig storage.")

    def find_and_remove_from_rig(self, item: BaseAsset, source: Rig):
        """Find and remove the item from the target Rig."""
        if item in source.storage:
            source.storage.remove(item)
        else:
            print(f"{item.name} not found in {source.name} storage.")

    # ---------- Core Methods ----------

    def acquire_rig(self):
        """Remove a CryptoToken and assign a Rig."""
        if self.find_and_remove_from_inventory(CryptoToken):  # Uses helper function to find and remove CryptoToken
            self.rig = Rig("Hail Mary")
            print("Rig acquired.")
        else:
            print("No CryptoToken available to acquire rig.")

    def launch_data_spikes(self, target: Rig):
        """Launch a DataSpike at a target Rig."""
        if not isinstance(target, Rig):
            print("Target is not a rig")
            return

        spike = self.find_and_remove_from_inventory(DataSpike)
        if spike:
            target.damage_counter += 1
            print("DataSpike launched")
        else:
            print("No DataSpike available.")

    def encrypt_assets(self):
        """Encrypts assets using a SecurityChip, if available."""
        self.inventory_encrypted = False
        self.rig_storage_encrypted = False
        self.chip = None
        self.chip_location = None

        chip_info = self.find_item_type(SecurityChip)
        if not chip_info:
            print("Security chip needed to encrypt assets.")
            return

        self.chip, self.chip_location = chip_info

        self.inventory_encrypted = self.encrypt_items(self.inventory)
        self.rig_storage_encrypted = self.encrypt_items(self.rig.storage) if self.rig else False

        if self.inventory_encrypted or self.rig_storage_encrypted:
            if self.inventory_encrypted and self.rig_storage_encrypted:
                print("Assets from inventory and rig's storage have been encrypted.")
            elif self.inventory_encrypted:
                print("Assets from inventory have been encrypted.")
            elif self.rig_storage_encrypted:
                print("Assets from rig's storage have been encrypted.")
            self.remove_security_chip()
        else:
            print("No assets have been encrypted.")

    def decrypt_target_rig(self, target: Rig):
        """ Decrypt assets in a target Rig, if it is broken and a SecurityChip is available. """
        if not isinstance(target, Rig):
            print("Target is not a valid Rig.")
            return
        if not target.broken_state:
            print(f"Cannot decrypt {target.name}: target rig is not broken/exposed.")
            return

        chip_info = self.find_item_type(SecurityChip)
        if not chip_info:
            print("Security Chip needed to decrypt target rig assets.")
            return

        self.chip, self.chip_location = chip_info

        decrypted_any = self.decrypt_items(target.storage)

        if decrypted_any:
            self.remove_security_chip()
            print("Target assets have been decrypted successfully.")
        else:
            print("Assets are already decrypted. SecurityChip not consumed.")

    def upgrade_rig(self):
        """ Upgrade the Hacker's rig """

        # Check that Hacker has a rig
        if not self.rig:
            print("Hacker does not have a rig to upgrade.")
            return

        # Search for Hardware Patch
        hardware_patch_info = self.find_item_type(HardwarePatch)
        if not hardware_patch_info:
            print("Hardware Patch needed to upgrade rig.")
            return

        patch, location = hardware_patch_info
        if location == "inventory":
            self.inventory.remove(patch)
        else:
            self.rig.storage.remove(patch)

        print(f"{self.rig.name} has been upgraded.")

    # Store assets from target rig.
    def store_assets(self, item: BaseAsset, source: Rig, destination):
        """
        Move an asset from the source rig's storage to the hackers inventory or the hacker's rig's storage.
        destination (list): The target storage location can be either self.inventory or self.rig.storage.
        """
        if destination == self.inventory:
            self.inventory.append(item)
            self.find_and_remove_from_rig(item, source)
            print(f"{item.name} moved to inventory.")
        elif self.rig and destination == self.rig.storage:
            self.rig.storage.append(item)
            self.find_and_remove_from_rig(item, source)
            print(f"{item.name} moved to rig storage.")
        else:
            print("Invalid destination for storing asset.")
