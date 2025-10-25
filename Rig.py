"""
File: Rig.py
Description: Defines the Rig class
Author: Erica Box
ID: 110468687
Username: boxey001
This is my own work as defined by the University's Academic Misconduct Policy.
"""
import random as rand
import time

from Asset import DataSpike, SecurityChip, CryptoToken, HardwarePatch, RemovableDrive


class Rig:
    def __init__(self, name: str):
        self.name = name
        self.damage_counter = 0
        self.broken_state = False
        self.storage = [DataSpike(),
                        DataSpike(),
                        RemovableDrive()]
        self.upgrade_level = 0
        self.last_generation_time = time.time()
        self.generation_interval = 15

    # ---------- Helper Methods ----------

    def max_damage_capacity(self) -> int:
        """
        Return how many hits the rig can take before breaking.
        """

        return 2 + self.upgrade_level

    def max_storage_capacity(self) -> int:
        """
        Return how many items the rig can store.
        """

        return 3 + (self.upgrade_level * 2)

    # ---------- Core Methods ----------

    def rig_repair(self):
        """
        Rig can be repaired using an upgrade level. When a rig is repaired, its damage_counter returns
        to 0, and its broken_state returns to False.
        Rig repairs cost one upgrade_level.
        """

        # 1. Check that an upgrade level is available
        if self.upgrade_level == 0:
            print(f'Upgrade level is not available for rig repair.')
            return

        # 2. Repair rig
        if self.damage_counter > 0:
            self.damage_counter = 0
            self.broken_state = False
            self.upgrade_level -= 1
            print(f'Rig repair complete. 1 upgrade level consumed.')
        else:
            print(f"No repair is needed.")

    def rig_upgrade(self):
        """
        Upgrades the Hacker's rig.
        """

        self.upgrade_level += 1

    def rigs_condition(self):
        """
        Returns the condition of the rig.
        """

        if self.broken_state:
            condition = "Broken"
        else:
            condition = "Pristine"
        print(f"{condition} (Level {self.upgrade_level})")

    def generate_assets(self):
        """
        Generates a random asset and adds it to this rig's storage,
        respecting the storage capacity.
        """

        current_time = time.time()
        time_elapsed = current_time - self.last_generation_time

        # Check if enough time has passed for one asset
        if time_elapsed >= self.generation_interval:
            # Check storage capacity
            if len(self.storage) >= self.max_storage_capacity():
                print("Storage full. Cannot generate new assets.")
                return

            # Generate one random asset
            asset_types = {
                "CryptoToken": CryptoToken,
                "DataSpike": DataSpike,
                "RemovableDrive": RemovableDrive,
                "SecurityChip": SecurityChip,
                "HardwarePatch": HardwarePatch
            }

            random_key = rand.choice(list(asset_types.keys()))
            asset_class = asset_types[random_key]
            new_asset = asset_class()
            self.storage.append(new_asset)
            print(f"Background generation: {new_asset.name} added to storage.")

            # Reset timer for next generation
            self.last_generation_time = current_time
