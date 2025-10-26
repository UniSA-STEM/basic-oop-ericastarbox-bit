"""
File: Rig.py
Description: Defines the Rig class and related methods required for the Basic Programming Assignment.
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
        self._check_generation()  # Auto-check whenever accessed
        return 2 + self.upgrade_level

    def max_storage_capacity(self) -> int:
        """
        Return how many items the rig can store.
        """
        self._check_generation()  # Auto-check whenever accessed
        return 3 + (self.upgrade_level * 2)

    def _check_generation(self):
        """
        Checks and generates assets in the background.
        """
        current_time = time.time()
        time_elapsed = current_time - self.last_generation_time

        if time_elapsed >= self.generation_interval:
            if len(self.storage) < self.max_storage_capacity():
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
                self.last_generation_time = current_time

    def update_broken_state(self):
        if self.damage_counter >= self.max_damage_capacity():
            self.broken_state = True
            print(f"Rig {self.name} is broken.")
        else:
            self.broken_state = False
        return self.broken_state

    def rig_storage(self):
        """
        Prints a clear string representation of the rig's storage.
        """

        storage_names = ", ".join([item.name for item in self.rig_storage()])
        return storage_names

    # ---------- Core Methods ----------

    def rig_repair(self):
        """
        Rig can be repaired using an upgrade level. When a rig is repaired, its damage_counter returns
        to 0, and its broken_state returns to False.
        Rig repairs cost one upgrade_level.
        """
        self._check_generation()  # Check for asset generation

        if self.upgrade_level == 0:
            print(f'Upgrade level is not available for rig repair.')
            return

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
        self._check_generation()  # Check for asset generation
        self.upgrade_level += 1

    def rigs_condition(self):
        """
        Returns the condition of the rig.
        """
        self._check_generation()  # Check for asset generation

        if self.broken_state:
            condition = "Broken"
        else:
            condition = "Pristine"
        print(f"{condition} (Level {self.upgrade_level})")

    def generate_assets(self):
        """
        Manually trigger asset generation check.
        """
        self._check_generation()

    def __str__(self):
        """
        Returns a string representation of the rig, describing its condition and storage contents.
        """

        condition = "Broken" if self.broken_state else "Pristine"
        storage_items = ", ".join([item.name for item in self.storage]) if self.storage else "(empty)"
        return (
            "=====================\n"
            f"Rig Name: {self.name}\n"
            f"Condition: {condition}\n"
            f"Upgrade Level: {self.upgrade_level}\n"
            f"Storage: {storage_items}\n"
            "=====================\n"
        )
