"""
File: main.py
Description: <A brief description of this Python module.>
Author: Erica Box
ID: 110468687
Username: boxey001
This is my own work as defined by the University's Academic Misconduct Policy.
"""

from Rig import Rig
from Hacker import Hacker
from Asset import CryptoToken, SecurityChip, DataSpike, BaseAsset, HardwarePatch, RemovableDrive


# ---------- HELPER FUNCTIONS ----------

def validate_numeric_input(prompt, valid_options, error_message="Invalid choice. Please try again."):
    """
    Helper function to validate numeric input from the player.
    """

    while True:
        user_input = input(prompt)

        # Check if input is a digit
        if not user_input.isdigit():
            print(f"{error_message} Please enter a number.\n")
            continue

        # Convert to integer
        choice = int(user_input)

        # Check if choice is in valid options
        if choice in valid_options:
            return choice
        else:
            print(f"{error_message} Valid options are: {', '.join(map(str, valid_options))}\n")


# ---------- CORE FUNCTIONS ----------

# ----------------------------
# WELCOME MESSAGE AND SETUP
# ----------------------------
def welcome_message():
    """
    Displays the welcome message for the INTO THE GRID game and provides
    instructions for gameplay. This includes an overview of inventory items, in-game
    mechanics, and the player's objectives. The message also explains how the trace
    level impacts gameplay and provides the starting conditions for the game.
    """

    print(f"\nWelcome to INTO THE GRID.")
    input("""
    -  Your INVENTORY holds portable assets you carry:
       - CryptoTokens: currency to acquire or repair rigs
       - DataSpikes: offensive programs to damage target rigs
       - SecurityChips: required to encrypt or decrypt assets
       - HardwarePatches: upgrade components for your rig

    -  Your RIG has its own STORAGE (starts with 2 DataSpikes and 1 Removable Drive).
       Encrypted assets cannot be stolen, moved, or used until decrypted.

    -  TRACE LEVEL: increases with risky actions (attacking, encrypting, decrypting).
       If it reaches 5, you're exposed and blocked from taking actions.
       Trace decreases slowly over time as you lay low.

    -  OBJECTIVE: Build and defend your rig while breaking into others'.
       - Acquire a rig using a CryptoToken
       - Store and retrieve assets between inventory and rig storage
       - Encrypt assets to protect them; decrypt to use them again
       - Launch DataSpikes to damage enemy rigs
       - When a rig breaks, steal its unencrypted assets
       - Upgrade your rig with HardwarePatches for better storage and durability
       - Manage your trace level to stay operational

       Press ENTER to begin.
       """)


# ----------------------------
# NEW PLAYER SETUP
# ----------------------------
def new_player_setup():
    player_name = input("Please enter your hacker alias: ")
    player = Hacker(player_name)
    print(f"\nOkay Neo, let's get started. Your stats are as follows:\n\n{player}")
    print(f"Inventory: {player.inventory_items()}\n=====================\n")
    input(f"Press ENTER to acquire your rig and begin your journey.\n")
    rig = player.acquire_rig()
    print(f"\nYou have successfully purchased a rig. See your rig's stats below:\n\n{player.rig}\n")
    return player


# ----------------------------
# ASSET MANAGEMENT MENU
# ----------------------------
def asset_management(player):
    """
    Manages asset-related operations for a player, including inventory
    management, rig storage interaction, and asset encryption/decryption.
    """

    print("""
        ASSET MANAGEMENT
        ----------------
        1.) View inventory
        2.) View rig storage
        3.) Move items between inventory and rig storage
        4.) Encrypt assets
        5.) Decrypt assets
        """)

    choice = validate_numeric_input(
        "Enter your choice (1–5): ",
        [1, 2, 3, 4, 5],
        "Invalid option."
    )

    if choice == 1:
        player.inventory_items()

    elif choice == 2:
        player.rig_storage_items()

    elif choice == 3:
        source = validate_numeric_input(
            """
        Where do you want to move the item from:
        1.) Inventory
        2.) Rig's storage
        Enter choice: """,
            [1, 2],
            "Invalid source location."
        )

        if source == 1:
            source_location = "inventory"
            source_items = player.inventory.items
            source_address = player.inventory
        else:
            source_location = "rig storage"
            source_items = player.rig.storage
            source_address = player.rig.storage

        item = input(f"""
        Which of the following items do you want to move from {source_location}: 
        {source_items}
        Enter item: """)

        player.retrieve_assets(item, source_address)

    elif choice == 4:
        encrypt_from = validate_numeric_input(
            """
        Where do you want to encrypt assets from:
        1.) Inventory
        2.) Rig's storage
        Enter choice: """,
            [1, 2],
            "Invalid location."
        )

        if encrypt_from == 1:
            source_address = player.inventory
        else:
            source_address = player.rig.storage

        player.encrypt_assets(source_address)

    elif choice == 5:
        decrypt_from = validate_numeric_input(
            """
        Where do you want to decrypt assets from:
        1.) Inventory
        2.) Rig's storage
        Enter choice: """,
            [1, 2],
            "Invalid location."
        )

        if decrypt_from == 1:
            source_address = player.inventory
        else:
            source_address = player.rig.storage

        player.decrypt_assets(source_address)


# ----------------------------
# MAIN GAMEPLAY LOOP
# ----------------------------
def play_game():
    welcome_message()
    player = new_player_setup()
    print("Please select from the following options to continue")

# asset_management(player)
