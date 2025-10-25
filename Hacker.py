"""
File: Hacker.py
Description: Defines the Hacker class and related methods required for the Basic Programming Assignment.
Author: Erica Box
ID: 110468687
Username: boxey001
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from _ast import Tuple
from typing import Optional
from Asset import CryptoToken, SecurityChip, DataSpike, BaseAsset, HardwarePatch
from Rig import Rig


class Hacker:
    def __init__(self, name: str):
        self.name = name
        self.inventory = [CryptoToken("CryptoToken", "Used to acquire rigs.")]
        self.rig = None
        self.trace_level = 0
        self.chip_location = None

    # ---------- Helper Methods ----------

    def find_and_remove_from_inventory(self, item_type):
        """
        Find and remove the first instance of the specified type in the Hacker's inventory.
        """
        for item in self.inventory:
            if isinstance(item, item_type):
                self.inventory.remove(item)
                return item
        return None

    def find_item_type(self, item_class: type) -> Optional[Tuple[BaseAsset, str]]:
        """
        Search for instance of item_class - a subclass of BaseAsset.
        First checks inventory and if not found, then rig.
        Returns a tuple of (item, location) or None if not found.
        """
        for item in self.inventory:
            if isinstance(item, item_class):
                return item, "inventory"
        if self.rig:
            for item in self.rig.storage:
                if isinstance(item, item_class):
                    return item, "rig"
        return None

    def find_and_remove_from_rig(self, items: BaseAsset, source: Rig):
        """
        Find and remove the item from the target Rig.
        """

        if items in source.storage:
            source.storage.remove(items)
            return True
        else:
            print(f"{items} not found in {source.name} storage.")
            return False

    def remove_item(self, item: BaseAsset, location):
        for asset in location:
            if item == asset and not item.encrypted:
                location.remove(asset)
                print(f"{item.name} removed.")

    # ---------- Core Methods ----------

    def acquire_rig(self):
        """
        Remove a CryptoToken and assign a Rig.
        """

        if self.find_and_remove_from_inventory(CryptoToken):  # Uses helper function to find and remove CryptoToken
            self.rig = Rig("Hail Mary")
            print("Rig acquired.")
        else:
            print("No CryptoToken available to acquire rig.")

    def launch_data_spikes(self, target: Rig):
        """
        Launch a DataSpike at a target Rig.
        """

        if not isinstance(target, Rig):
            print("Target is not a rig")
            return

        spike = self.find_and_remove_from_inventory(DataSpike)
        if spike:
            target.damage_counter += 1
            print("DataSpike launched")
        else:
            print("No DataSpike available.")

    def encrypt_assets(self, location):
        """
        Encrypts all assets in defined location.
        Location can be self.inventory or self.rig.storage.
        Encrypting assets requires one Security Chip
        """

        # 1. Ensure that chip is available.
        chip_found = self.find_item_type(SecurityChip)
        if not chip_found:
            print(f"Must have security chip to encrypt assets.")
            return

        chip, chip_location = chip_found
        chip_source = self.inventory if chip_location == "inventory" else self.rig.storage

        # 2. Track encryption
        any_encrypted = False
        location_str = "inventory" if location == self.inventory else "rig storage"

        # 3. Encrypt all unencrypted assets
        for asset in location:
            if not asset.encrypted:
                asset.encrypted = True
                any_encrypted = True

        # 4. Print results
        if any_encrypted:
            print(f"Assets in {location_str} have been encrypted.")
            self.remove_item(chip, self.inventory if chip_location == "inventory" else self.rig.storage)
        else:
            print(f"Assets in {location_str} are already encrypted. SecurityChip not consumed.")

    def decrypt_assets(self, target: Rig):
        """
        Decrypt assets in a target Rig, if it is broken and a SecurityChip is available.
        """

        # 1. Ensure that chip is available
        chip_found = self.find_item_type(SecurityChip)
        if not chip_found:
            print(f"Must have security chip to dencrypt assets.")
            return

        chip, chip_location = chip_found
        chip_source = self.inventory if chip_location == "inventory" else self.rig.storage

        # 2. Ensure target is a broken rig
        if not isinstance(target, Rig):
            print("Target is not a valid Rig.")
            return
        if not target.broken_state:
            print(f"Cannot decrypt {target.name}: target rig is not broken/exposed.")
            return

        # 3. Track decryption and decrypt all encrypted assets
        decrypted_any = False
        for asset in target.storage:
            if asset.encrypted:
                asset.encrypted = False
                decrypted_any = True

        # 4. Print results
        if decrypted_any:
            print("Target assets have been decrypted successfully.")
            self.remove_item(chip, self.inventory if chip_location == "inventory" else self.rig.storage)
        else:
            print("Assets are already decrypted. SecurityChip not consumed.")

    def upgrade_rig(self):
        """
        Upgrade the Hacker's rig
        """

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
    def store_asset(self, items: BaseAsset, source: Rig, destination: list):
        """
        Move asset(s) from the source rig's storage to the hackers inventory or the hacker's rig's storage.
        Asset(s) are turned to lists to allow for one or multiple assets to be moved at a time.
        destination (list): The target storage location can be either self.inventory or self.rig.storage.
        """

        if not isinstance(items, list):
            items = [items]

        for item in items:
            was_removed = self.find_and_remove_from_rig(item, source)
            if was_removed:
                destination.append(item)
                print(f"{item.name} moved to {('inventory' if destination == self.inventory else 'rig storage')}.")

    def retrieve_assets(self, item: BaseAsset, to_inventory: bool = False):
        """
        Move assets between the hacker's inventory and rig's storage.
        If to_inventory is True, assets are moved from storage to inventory.
        If to_inventory is False, assets are moved from inventory to storage.
        """

        # First, check that the hacker has a rig.
        if not self.rig:
            print("Hacker does not have a rig.")
            return

        # Move asset from storage to inventory
        if to_inventory:
            for asset in self.rig.storage:
                if item == asset:
                    if asset.encrypted:
                        print("Cannot store encrypted asset.")
                        return
                    self.rig.storage.remove(asset)
                    self.inventory.append(asset)
                    print(f"{item.name} retrieved from storage and placed in inventory.")
                    return
            print(f"{item.name} not found in rig storage.")
            return

        # Move asset from inventory to storage
        else:
            for asset in self.inventory:
                if item == asset:
                    if asset.encrypted:
                        print("Cannot retrieve encrypted asset.")
                        return
                    self.inventory.remove(asset)
                    self.rig.storage.append(asset)
                    print(f"{item.name} retrieved from inventory and placed in rig's storage.")
                    return
            print(f"{item.name} not found in inventory.")

    def scan_inventory(self, item: BaseAsset):
        """ Scan inventory for specific assets.
        If found, remove asset from inventory and return asset.
        """

        for asset in self.inventory:
            if item == asset:
                self.inventory.remove(asset)
                print(f"Removed asset {item.name} from inventory.")
                return item
        print(f"{item.name} not found in inventory.")
        return None

    def __str__(self):
        return (
            "=====================\n"
            f"Hacker Name: {self.name}\n"
            f"{f'Rig Name: {self.rig.name}' if self.rig else 'Hacker has no rig.'}\n"
            f"Trace Level: {self.trace_level}\n"
            "=====================\n"
        )
