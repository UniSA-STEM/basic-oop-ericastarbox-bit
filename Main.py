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

# --------------------------
# WELCOME MESSAGE AND SETUP
# --------------------------
def welcome_message():
    """
    Displays the welcome message for the INTO THE GRID game and provides
    instructions for gameplay. This includes an overview of inventory items, in-game
    mechanics, and the player's objectives. The message also explains how the trace
    level impacts gameplay and provides the starting conditions for the game.
    """

    print(f"\nWelcome to INTO THE GRID.")
    input("""
    You are a hacker navigating the digital underworld in search of power, data,
    and survival.  Your rig is your lifeline - upgrade it, protect it, and use it
    to attack others on the Grid.

    --- GAME OVERVIEW ---
    
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


# -----------------
# NEW PLAYER SETUP
# -----------------
def new_player_setup():
    player_name = input("Please enter your hacker alias: ")
    player = Hacker(player_name)
    print(f"\nOkay {player_name}, let's get started. Your stats are as follows:\n")
    print(f"\n" + "=" * 40)
    print("PLAYER PROFILE")
    print(f"=" * 40)
    print(player)
    print(f"-" * 40)
    print("Inventory:", player.inventory_items())
    print(f"=" * 40 + "\n")
    input(f"Press ENTER to acquire your rig and begin your journey.\n")
    rig = player.acquire_rig()
    print(f"\nYou have successfully purchased a rig. See your rig's stats below:\n{player.rig}")
    return player


# ----------------------
# ASSET MANAGEMENT MENU
# ----------------------
def asset_management(player):
    """
    Manages asset-related operations for a player, including inventory
    management, rig storage interaction, and asset encryption/decryption.
    """

    print("""
    ========================================
    ASSET MANAGEMENT
    ========================================
        1.) View inventory
        2.) View rig storage
        3.) Move items between inventory and rig storage
        4.) Encrypt assets
        5.) Decrypt assets
        6.) Return to main menu
    ========================================
    """)

    choice = validate_numeric_input(
        "Enter your choice (1–6): ",
        [1, 2, 3, 4, 5, 6],
        "Invalid option."
    )

    # 1. View inventory
    to_inventory = player.inventory if choice == 3 else player.rig.storage
    if choice == 1:
        print(f"\nInventory: {player.inventory_items()}")

        # Return to asset management menu
        asset_management(player)

    # 2. View rig storage
    elif choice == 2:
        if player.rig:
            storage_items = ", ".join([item.name for item in player.rig.storage]) if player.rig.storage else "(empty)"
            print(f"\nRig Storage: {storage_items}")
        else:
            print("\nYou don't have a rig yet.")

        # Return to asset management menu
        asset_management(player)

    # 3. Move items between inventory and rig storage
    elif choice == 3:
        source = validate_numeric_input(
            """
            Where do you want to move the item from:
            1.) Inventory
            2.) Rig's storage
            Enter choice (1-2): """,
            [1, 2],
            "Invalid source location."
        )

        if source == 1:
            source_location = "inventory"
            source_address = player.inventory

        else:
            source_location = "rig storage"
            source_address = player.rig.storage

        item = input(f"""
        Which of the following items do you want to move from {source_location}:
        {', '.join(item.name for item in source_address)}
        Enter item name: 
        """)

        # Find the item in the source location and move to the destination
        item_to_move = next((asset for asset in source_address if asset.name == item), None)
        if item_to_move:
            player.retrieve_assets(item_to_move, to_inventory)
        else:
            print(f"Item '{item}' not found in {source_location}.")

        # Return to asset management menu
        asset_management(player)

    # 4. Encrypt assets
    elif choice == 4:
        encrypt_from = validate_numeric_input(
            """
        Where do you want to encrypt assets from:
        1.) Inventory
        2.) Rig's storage
        Enter choice (1-2): """,
            [1, 2],
            "Invalid location."
        )

        if encrypt_from == 1:
            source_address = player.inventory
        else:
            source_address = player.rig.storage

        player.encrypt_assets(source_address)

        # Return to asset management menu
        asset_management(player)

    # 5. Decrypt assets
    elif choice == 5:
        decrypt_from = validate_numeric_input(
            """
        Where do you want to decrypt assets from:
        1.) Inventory
        2.) Rig's storage
        Enter choice (1-2): """,
            [1, 2],
            "Invalid location."
        )

        if decrypt_from == 1:
            source_address = player.inventory
        else:
            source_address = player.rig.storage

        player.decrypt_assets(source_address)

        # Return to asset management menu
        asset_management(player)

    # 6. Return to main menu
    else:
        main_menu(player)


# ------------
# BATTLE MODE
# ------------
def battle_mode(player):
    """
    Triggers battle mode, interacting with the user and processing their input.
    """
    acquired_assets = []
    target = Rig("Newman")
    print("\nAN ALERT: An enemy rig is approaching!\nSignature matches: NEWMAN.\n")

    choice = validate_numeric_input(
        "Do you want to engage?\n"
        "1.) Yes\n"
        "2.) No\n"
        "Enter your choice (1-2): ",
        [1, 2],
        "Invalid option."
    )

    if choice == 1:
        # Initial attack
        player.launch_data_spikes(target)
        target.target_damage()
        print(target.__str__(True))

        # Continue battle loop
        while not target.broken_state:
            # Ask if player wants to continue BEFORE next attack
            continue_battle = validate_numeric_input(
                "Do you want to continue the battle?\n"
                "1.) Yes\n"
                "2.) No\n"
                "Enter your choice (1-2): ",
                [1, 2],
                "Invalid option."
            )

            if continue_battle == 2:
                print("Retreating from battle...")
                main_menu(player)
                return  # Exit the function

            # If yes, launch another attack
            player.launch_data_spikes(target)
            target.target_damage()
            print(target.__str__(True))

        # Target is broken
        if target.broken_state:
            print(f">>> Rig {target.name} is BROKEN! <<<\n")
            choice = validate_numeric_input(
                "What do you want to do next?\n"
                "1.) Take target's assets\n"
                "2.) Abandon broken rig and return to main menu\n"
                "Enter your choice (1-2): ",
                [1, 2],
                "Invalid option."
            )
            if choice == 1:
                # Move assets from target's storage to player's inventory
                for asset in target.storage[:]:  # Use slice to avoid modification during iteration
                    target.storage.remove(asset)
                    player.inventory.append(asset)
                    acquired_assets.append(asset.name)
                print(f"\nAcquired {acquired_assets} from target's rig.")
                main_menu(player)
            else:
                print("Abandoning broken rig and returning to the main menu...")
                main_menu(player)

    else:
        print("\nOkay, we'll stay put...")
        main_menu(player)


# -----------
# MAIN MENU
# -----------
def main_menu(player):
    print("""
    Please select from the following options to continue: 
    
    ========================================
    MAIN MENU
    ========================================
    1.) Asset Management
    2.) Upgrade Rig
    3.) Battle Mode
    ========================================
    """)

    choice = validate_numeric_input(
        "Enter your choice (1–3): ",
        [1, 2, 3],
        "Invalid option."
    )

    if choice == 1:
        asset_management(player)

    elif choice == 2:
        player.upgrade_rig()
        main_menu(player)

    else:
        battle_mode(player)


# ---------------
# GAMEPLAY LOOP
# ---------------
def play_game():
    welcome_message()
    player = new_player_setup()
    main_menu(player)


play_game()
