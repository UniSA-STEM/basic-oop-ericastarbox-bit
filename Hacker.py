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

    def launch_data_spikes(self):
