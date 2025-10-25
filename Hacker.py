"""
File: Hacker.py
Description: Defines the Hacker class and related methods required for the Basic Programming Assignment.
Author: Erica Box
ID: 110468687
Username: boxey001
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from typing import Tuple, Optional
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

    def remove_item(self, item: BaseAsset, location: list[BaseAsset]) -> BaseAsset | None:
        """
        Removes an unencrypted asset from the specified location (inventory or rig storage).
        If successful, returns removed asset, otherwise returns None.
        """

        for asset in location:
            if item == asset:
                if item.encrypted:
                    print(f"{item.name} can't be removed because it's encrypted.")
                    return None
                location.remove(asset)
                print(f"{item.name} removed.")
                return item

        print(f"{item.name} not found.")
        return None

    # ---------- Core Methods ----------

    def acquire_rig(self):
        """
        Remove a CryptoToken and assign a Rig.
        """

        # 1. Ensure CryptoToken is available.
        token_found = self.find_item_type(CryptoToken)
        if not token_found:
            print(f"Must have CryptoToken to encrypt assets.")
            return

        # 2. Unpack the tuple returned from find_item_type()
        #    'token' = the CryptoToken object
        #    'token_location' = where object was found
        token, token_location = token_found
        token_source = self.inventory if token_location == "inventory" else self.rig.storage

        # 3. Remove token from source location and acquire Rig
        self.remove_item(token, token_source)

        # 4. Acquire Rig
        self.rig = Rig("Hail Mary")
        print("Rig acquired for one CryptoToken.")

    def launch_data_spikes(self, target: Rig):
        """
        Launch a DataSpike at a target Rig.
        """

        # 1. Check that target is an instance of Rig.
        if not isinstance(target, Rig):
            print("Target is not a rig")
            return

        # 2. Check that DataSpike is available
        spike_found = self.find_item_type(DataSpike)
        if not spike_found:
            print(f"No DataSpike found")
            return

        # 3. Damage target and consume DataSpike
        spike, spike_location = spike_found
        self.remove_item(spike, self.inventory if spike_location == "inventory" else self.rig.storage)
        target.damage_counter += 1
        print("DataSpike launched.")

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
            print(f"Must have security chip to decrypt assets.")
            return

        chip, chip_location = chip_found

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
    def store_asset(self, items: BaseAsset | list[BaseAsset], source: Rig, destination: list[BaseAsset]):
        """
        Move asset(s) from the source rig's storage to the hackers inventory or the hacker's rig's storage.
        destination (list): The target storage location can be either self.inventory or self.rig.storage.
        """

        # 1. Turn items into list to allow for one or multiple assets to be moved at a time.
        if not isinstance(items, list):
            items = [items]

        # 2. Ensure that the specified source is a Rig.
        if not isinstance(source, Rig):
            print("Source must be an instance of Rig.")
            return

        # 3. Remove items from source and move to destination.
        for item in items:
            removed_items = self.remove_item(item, source)
            if removed_items:
                destination.append(item)
                print(f"{removed_items} moved to {('inventory' if destination == self.inventory else 'rig storage')}.")

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
