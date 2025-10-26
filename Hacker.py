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
import time


class Hacker:
    def __init__(self, name: str):
        self.name = name
        self.inventory = [CryptoToken()]
        self.rig = None
        self.trace_level = 0
        self.chip_location = None
        self.trace_level_reduced_time = time.time()
        self.trace_level_reduced_interval = 15

    # ---------- Helper Methods ----------

    def find_item_type(self, item_class: type) -> Optional[Tuple[BaseAsset, str]]:
        """
        Search for an instance of item_class - a subclass of BaseAsset.
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

    def remove_item(self, item: BaseAsset, location: list) -> BaseAsset | None:
        """
        Removes an unencrypted asset from the specified location (inventory or rig storage).
        If successful, returns the removed asset, otherwise returns None.
        """

        # 1. Check that the item is in the location.
        if item not in location:
            print(f"{item.name} not found.")
            return None

        # 2. Check that the item is not encrypted.
        if item.encrypted:
            print(f"{item.name} can't be removed because it's encrypted.")
            return None

        # 3. Remove the item from the location and return it.
        location.remove(item)
        return item

    def adjust_trace_level(self, amount: int = 1):
        """
        Adjusts the trace level by a specified amount.
        """

        self.trace_level += amount
        print(f"\n!!! TRACE ALERT !!! Trace level increased to {self.trace_level} out of {self.trace_level_limit()}!\n")

    @staticmethod
    def trace_level_limit():
        """
        Specifies and returns the hacker's trace level limit.
        """
        trace_level_limit = 5
        return trace_level_limit

    def reduce_trace_level(self):
        """
        Slowly reduces the hacker's trace level in the background.
        """

        current_time = time.time()
        time_elapsed = current_time - self.trace_level_reduced_time

        if time_elapsed >= self.trace_level_reduced_interval:
            if self.trace_level > 0:
                self.trace_level -= 1
                print(f"Background recovery: trace level reduced to {self.trace_level}.")
                self.trace_level_reduced_time = current_time

    def inventory_items(self):
        """
        Prints a clear string representation of the hacker's inventory.
        """

        inventory_names = ", ".join([item.name for item in self.inventory])
        return inventory_names

    # ---------- Core Methods ----------

    def acquire_rig(self):
        """
        Remove a CryptoToken and assign a Rig.
        """

        # 1. Ensure CryptoToken is available.
        token_found = self.find_item_type(CryptoToken)
        if not token_found:
            print(f"\nMust have CryptoToken to acquire a rig.")
            return

        # 2. Unpack the tuple returned from find_item_type()
        #    'token' = the CryptoToken object
        #    'token_location' = where the object was found
        token, token_location = token_found
        token_source = self.inventory if token_location == "inventory" else self.rig.storage

        # 3. Remove token from the source location and acquire Rig
        self.remove_item(token, token_source)

        # 4. Acquire Rig
        self.rig = Rig("Hail Mary")

        # 5. Decrease trace level in the background
        self.reduce_trace_level()

    def launch_data_spikes(self, target: Rig):
        """
        Launch a DataSpike at a target Rig.
        """

        # 1. Check that the hacker's trace level does not exceed the limit.
        if self.trace_level >= self.trace_level_limit():
            print(f"Trace level limit reached. Cannot launch DataSpike.")
            return

        # 2. Check that the target is an instance of Rig.
        if not isinstance(target, Rig):
            print("Target is not a rig")
            return

        # 3. Check that DataSpike is available
        spike_found = self.find_item_type(DataSpike)
        if not spike_found:
            print(f"No DataSpike found")
            return

        # 4. Damage target, consume DataSpike, and increase trace level
        spike, spike_location = spike_found
        spike_source = self.inventory if spike_location == "inventory" else self.rig.storage
        self.remove_item(spike, spike_source)
        target.damage_counter += 1
        self.adjust_trace_level(2)  # Increase the trace level by two
        print("DataSpike launched.")

        # 5. Check the broken state of the target
        target.update_broken_state()
        if target.broken_state:
            print(f"Target's assets may be retrieved.")

    def encrypt_assets(self, location):
        """
        Encrypts all assets in a defined location.
        Location can be self.inventory or self.rig.storage.
        Encrypting assets requires one Security Chip
        """

        # 1. Check that the hacker's trace level does not exceed the limit.
        if self.trace_level >= self.trace_level_limit():
            print(f"Trace level limit reached. Cannot encrypt assets.")
            return

        # 2. Ensure that the chip is available.
        chip_found = self.find_item_type(SecurityChip)
        if not chip_found:
            print(f"\nMust have security chip to encrypt assets.")
            return

        chip, chip_location = chip_found
        chip_source = self.inventory if chip_location == "inventory" else self.rig.storage

        # 3. Track encryption
        any_encrypted = False
        location_str = "inventory" if location == self.inventory else "rig storage"

        # 4. Encrypt all unencrypted assets
        for asset in location:
            if not asset.encrypted:
                asset.encrypted = True
                any_encrypted = True

        # 5. Print results and adjust trace level
        if any_encrypted:
            self.adjust_trace_level(1)  # Increase trace level by 1
            print(f"Assets in {location_str} have been encrypted.")
            self.remove_item(chip, chip_source)
        else:
            print(f"Assets in {location_str} are already encrypted. SecurityChip not consumed.")

    def decrypt_assets(self, target: Rig):
        """
        Decrypt assets in a target Rig if it is broken and a SecurityChip is available.
        """

        # 1. Check that the hacker's trace level does not exceed the limit.
        if self.trace_level >= self.trace_level_limit():
            print(f"Trace level limit reached. Cannot decrypt assets.")
            return

        # 2. Ensure that chip is available
        chip_found = self.find_item_type(SecurityChip)
        if not chip_found:
            print(f"\nMust have security chip to decrypt assets.")
            return

        chip, chip_location = chip_found
        chip_source = self.inventory if chip_location == "inventory" else self.rig.storage

        # 3. Ensure the target is a broken rig
        if not isinstance(target, Rig):
            print("Target is not a valid Rig.")
            return
        if not target.broken_state:
            print(f"Cannot decrypt {target.name}: target rig is not broken/exposed.")
            return

        # 4. Track decryption and decrypt all encrypted assets
        decrypted_any = False
        for asset in target.storage:
            if asset.encrypted:
                asset.encrypted = False
                decrypted_any = True

        # 5. Increase trace level by 1
        self.adjust_trace_level(1)

        # 6. Print results
        if decrypted_any:
            print("Target assets have been decrypted successfully.")
            self.remove_item(chip, chip_source)
        else:
            print("Assets are already decrypted. SecurityChip not consumed.")

    def upgrade_rig(self):
        """
        Upgrade the Hacker's rig
        """

        # 1. Check that the hacker's trace level does not exceed the limit.
        if self.trace_level >= self.trace_level_limit():
            print(f"Trace level limit reached. Cannot upgrade rig.")
            return

        # 2. Check that Hacker has a rig
        if not self.rig:
            print("Hacker does not have a rig to upgrade.")
            return

        # 3. Search for Hardware Patch
        hardware_patch_info = self.find_item_type(HardwarePatch)
        if not hardware_patch_info:
            print("\nHardware Patch needed to upgrade rig.")
            return

        # 4. Remove Hardware Patch
        patch, location = hardware_patch_info
        patch_source = self.inventory if location == "inventory" else self.rig.storage
        removed_patch = self.remove_item(patch, patch_source)

        if not removed_patch:
            return

        # 5. Upgrade the rig
        self.rig.rig_upgrade()
        print(f"{self.rig.name} has been upgraded.")

        # 6. Decrease trace level in the background
        self.reduce_trace_level()

    def store_asset(self, items: BaseAsset | list[BaseAsset], source: Rig, destination):
        """
        Move asset(s) from the source rig's storage to the hacker's inventory or the hacker's rig's storage.
        destination (list): The target storage location can be either self.inventory or self.rig.storage.
        """

        # 1. Turn items into a list to allow for one or multiple assets to be moved at a time.
        if not isinstance(items, list):
            items = [items]

        # 2. Ensure that the specified source is a Rig.
        if not isinstance(source, Rig):
            print("Source must be an instance of Rig.")
            return

        # 3. Check if the source is a target rig (not the hacker's own rig) and if so, ensure it's broken
        if source != self.rig and not source.broken_state:
            print(f"Rig is not broken. Cannot remove items from {source.name}.")
            return

        # 4. Validate destination
        if destination != self.inventory and (not self.rig or destination != self.rig.storage):
            print("Invalid destination. Must be inventory or rig storage.")
            return

        # 5. Check storage capacity for rig destination before processing
        if self.rig and destination == self.rig.storage:
            current_count = len(self.rig.storage)
            max_capacity = self.rig.max_storage_capacity()
            available_space = max_capacity - current_count

            if available_space < len(items):
                print(f"Rig storage is full. Cannot store all items. Available space: {available_space}")
                return

        # 6. Remove items from the source and move to destination.
        for item in items:
            removed_item = self.remove_item(item, source.storage)

            if not removed_item:
                continue

            destination.append(removed_item)
            location_name = "inventory" if destination == self.inventory else "rig storage"
            print(f"{removed_item.name} moved to {location_name}.")

        # 7. Decrease trace level in the background
        self.reduce_trace_level()

    def retrieve_assets(self, item: BaseAsset, to_inventory: bool = False):
        """
        Move assets between the hacker's inventory and rig's storage.
        If to_inventory is True, assets are moved from storage to inventory.
        If to_inventory is False, assets are moved from inventory to storage.
        """

        # 1. Check that the hacker has a rig.
        if not self.rig:
            print("Hacker does not have a rig.")
            return

        # 2. Determine source and destination
        if to_inventory:
            source = self.rig.storage
            destination = self.inventory
        else:
            source = self.inventory
            destination = self.rig.storage

            # Check storage capacity when moving to rig
            current_count = len(self.rig.storage)
            max_capacity = self.rig.max_storage_capacity()
            if current_count >= max_capacity:
                print(f"Rig storage is full. Cannot store more items.")
                return

        # 3. Find and move the item
        location_from = "rig storage" if to_inventory else "inventory"
        location_to = "inventory" if to_inventory else "rig's storage"

        if item not in source:
            print(f"{item.name} not found in {location_from}.")
            return

        if item.encrypted:
            print(f"Cannot move encrypted asset.")
            return

        source.remove(item)
        destination.append(item)
        print(f"{item.name} retrieved from {location_from} and placed in {location_to}.")

        # 4. Decrease trace level in the background
        self.reduce_trace_level()

    def scan_inventory(self, item: BaseAsset):
        """
        Scan inventory for specific assets.
        If found, remove the asset from inventory and return the asset.
        """

        # Decrease trace level in the background
        self.reduce_trace_level()

        for asset in self.inventory:
            if item == asset:
                self.inventory.remove(asset)
                print(f"Removed asset {item.name} from inventory.")
                return item
        print(f"{item.name} not found in inventory.")
        return None

    def __str__(self):

        # Decrease trace level in the background
        self.reduce_trace_level()

        return (
            f"Hacker Name: {self.name}\n"
            f"Rig Name: {self.rig.name if self.rig else 'Hacker has no rig.'}\n"
            f"Trace Level: {self.trace_level}"
        )
