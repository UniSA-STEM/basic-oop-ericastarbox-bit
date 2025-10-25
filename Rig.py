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
        to 0, and its broken_state returns true.
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
        Displays the condition of the rig.
        """

        if self.broken_state:
            condition = "Broken"
        else:
            condition = "Pristine"

        return f"{condition} (Level {self.upgrade_level})"
