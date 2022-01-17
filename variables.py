import pygame

entity_types = [
    # [name, maxhp, left_image, right_image, size]
    ["Pig", 10, pygame.image.load("textures/entity/pig_left.png"), pygame.image.load("textures/entity/pig_right.png"), (50, 30)],
]

fuel_list = {
    6: 2,
    7: 0.5,
    13: 1.5,
    14: 2,
    19: 8,
    22: 8
}

furnace_recipes = {
    9: 17,
    10: 18,
    5: 1,
    6: 22,
}

color_modes = {
    "dark_mode": {
        "main_menu_background": pygame.image.load("textures/backgrounds/main_menu_dark.png"),
        "main_menu_text_shadow": (33,76,127),
        "main_menu_text": (63,106,157),
        "main_menu_button_bg": (15,50,64),
        "main_menu_button_border": (63,106,157),
        "main_menu_button_bg_hover": (35,70,84),
        "inv_slot_bg": (5,40,54),
        "inv_border": (63,106,157),
        "inv_bg": (15,50,64)
    },
    "light_mode": {
        "main_menu_background": pygame.image.load("textures/backgrounds/main_menu.png"),
        "main_menu_text_shadow": (0,0,0),
        "main_menu_text": (255,255,255),
        "main_menu_button_bg": (140, 140, 140),
        "main_menu_button_border": (40, 40, 40),
        "main_menu_button_bg_hover": (100, 100, 100),
        "inv_slot_bg": (140, 140, 140),
        "inv_border": (0,0,0),
        "inv_bg": (180,180,180)
    }

}

block_type = {
    1: {
        "name": "stone",
        "breaking_time": 5,
        "txt": pygame.image.load("textures/blocks/stone.png"),
        "type": "block",
        "drop": [5],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [1],
        "required_tool_level": 1
    },
    2: {
        "name": "grass",
        "breaking_time": 1,
        "txt": pygame.image.load("textures/blocks/grass_block.png"),
        "type": "block",
        "drop": [3],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [3],
        "required_tool_level": 0
    },
    3: {
        "name": "dirt",
        "breaking_time": 1,
        "txt": pygame.image.load("textures/blocks/dirt.png"),
        "type": "block",
        "drop": [3],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [3],
        "required_tool_level": 0
    },
    4: {
        "name": "bedrock",
        "breaking_time": 10000000,
        "txt": pygame.image.load("textures/blocks/bedrock.png"),
        "type": "block",
        "drop": [4],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [],
        "required_tool_level": 20
    },
    5: {
        "name": "cobblestone",
        "breaking_time": 5,
        "txt": pygame.image.load("textures/blocks/cobblestone.png"),
        "type": "block",
        "drop": [5],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [1],
        "required_tool_level": 1
    },
    6: {
        "name": "wood log",
        "breaking_time": 3,
        "txt": pygame.image.load("textures/blocks/oak_log.png"),
        "type": "block",
        "drop": [6],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [2],
        "required_tool_level": 0
    },
    7: {
        "name": "leaves",
        "breaking_time": 0,
        "txt": pygame.image.load("textures/blocks/oak_leaves.png"),
        "type": "block",
        "drop": [22],
        "amount": [0],
        "drop_probability": 0.1,
        "intended_tool": [5],
        "required_tool_level": 0
    },
    8: {
        "name": "diamond ore",
        "breaking_time": 5,
        "txt": pygame.image.load("textures/blocks/diamond_ore.png"),
        "type": "block",
        "drop": [16],
        "amount": [1],
        "drop_probability": 1,
        "fortune": True,
        "intended_tool": [1],
        "required_tool_level": 3
    },
    9: {
        "name": "gold ore",
        "breaking_time": 5,
        "txt": pygame.image.load("textures/blocks/gold_ore.png"),
        "type": "block",
        "drop": [9],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [1],
        "required_tool_level": 3
    },
    10: {
        "name": "iron ore",
        "breaking_time": 5,
        "txt": pygame.image.load("textures/blocks/iron_ore.png"),
        "type": "block",
        "drop": [10],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [1],
        "required_tool_level": 2
    },
    11: {
        "name": "coal ore",
        "breaking_time": 5,
        "txt": pygame.image.load("textures/blocks/coal_ore.png"),
        "type": "block",
        "drop": [19],
        "amount": [1,2],
        "drop_probability": 1.1,
        "fortune": True,
        "intended_tool": [1],
        "required_tool_level": 1
    },
    12: {
        "name": "lapis ore",
        "breaking_time": 5,
        "txt": pygame.image.load("textures/blocks/lapis_ore.png"),
        "type": "block",
        "drop": [20],
        "amount": [2,3,4],
        "drop_probability": 1,
        "fortune": True,
        "intended_tool": [1],
        "required_tool_level": 2
    },
    13: {
        "name": "wood plank",
        "breaking_time": 2,
        "txt": pygame.image.load("textures/blocks/oak_planks.png"),
        "type": "block",
        "drop": [13],
        "amount": [1],
        "drop_probability": 1,
        "crafting_recipe": [[[6]]],
        "crafting_amount": 4,
        "default_behind": False,
        "intended_tool": [2],
        "required_tool_level": 0
    },
    14: {
        "name": "crafting table",
        "breaking_time": 2,
        "txt": pygame.image.load("textures/blocks/crafting_table.png"),
        "type": "block",
        "drop": [14],
        "amount": [1],
        "drop_probability": 1,
        "crafting_recipe": [[[13,13],[13,13]]],
        "crafting_amount": 1,
        "default_behind": True,
        "intended_tool": [2],
        "required_tool_level": 0
    },
    15: {
        "name": "furnace",
        "breaking_time": 5,
        "txt": pygame.image.load("textures/blocks/furnace.png"),
        "type": "block",
        "drop": [15],
        "amount": [1],
        "drop_probability": 1,
        "crafting_recipe": [[[5,5,5],[5,0,5],[5,5,5]]],
        "crafting_amount": 1,
        "default_behind": True,
        "intended_tool": [1],
        "required_tool_level": 1
    },
    16: {
        "name": "diamond",
        "txt": pygame.image.load("textures/items/diamond.png"),
        "type": "item"
    },
    17: {
        "name": "gold ingot",
        "txt": pygame.image.load("textures/items/gold_ingot.png"),
        "type": "item"
    },
    18: {
        "name": "iron ingot",
        "txt": pygame.image.load("textures/items/iron_ingot.png"),
        "type": "item"
    },
    19: {
        "name": "coal",
        "txt": pygame.image.load("textures/items/coal.png"),
        "type": "item"
    },
    20: {
        "name": "lapis lazuli",
        "txt": pygame.image.load("textures/items/lapis_lazuli.png"),
        "type": "item"
    },
    21: {
        "name": "charcoal",
        "txt": pygame.image.load("textures/items/charcoal.png"),
        "type": "item"
    },
    22: {
        "name": "oak sapling",
        "breaking_time": 0.5,
        "txt": pygame.image.load("textures/blocks/oak_sapling.png"),
        "type": "block",
        "drop": [22],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [5],
        "required_tool_level": 0
    },
    23: {
        "name": "stick",
        "txt": pygame.image.load("textures/items/stick.png"),
        "type": "item",
        "crafting_recipe": [[[13],[13]]],
        "crafting_amount": 4
    },
    24: {
        "name": "amelinium",
        "txt": pygame.image.load("textures/items/amelinium.png"),
        "type": "item",
        "crafting_recipe": [[[16,17],[18,20]]],
        "crafting_amount": 1
    },
    25: {
        "name": "dimensioner",
        "breaking_time": 1.5,
        "txt": pygame.image.load("textures/blocks/dimensioner.png"),
        "type": "block",
        "crafting_recipe": [[[1,1],[1,1]]],
        "crafting_amount": 1,
        "default_behind": True,
        "drop": [25],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [1],
        "required_tool_level": 1
    },
    29: {
        "name": "shears",
        "txt": pygame.image.load("textures/items/shears.png"),
        "type": "item",
        "tool_type": 5,
        "tool_level": 3,
        "crafting_recipe": [[[18],[0,18]], [[0,18],[18]]],
        "crafting_amount": 1
    },
    30: {
        "name": "blue flower",
        "breaking_time": 0.5,
        "txt": pygame.image.load("textures/blocks/kwiat1.png"),
        "type": "block",
        "drop": [30],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [5],
        "required_tool_level": 0
    },
    31: {
        "name": "orange flower",
        "breaking_time": 0.5,
        "txt": pygame.image.load("textures/blocks/kwiat2.png"),
        "type": "block",
        "drop": [31],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [5],
        "required_tool_level": 0
    },
    32: {
        "name": "purple flower",
        "breaking_time": 0.5,
        "txt": pygame.image.load("textures/blocks/kwiat3.png"),
        "type": "block",
        "drop": [32],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [5],
        "required_tool_level": 0
    },
    33: {
        "name": "pink flower",
        "breaking_time": 0.5,
        "txt": pygame.image.load("textures/blocks/kwiat4.png"),
        "type": "block",
        "drop": [33],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [5],
        "required_tool_level": 0
    },
    34: {
        "name": "light blue flower",
        "breaking_time": 0.5,
        "txt": pygame.image.load("textures/blocks/kwiat5.png"),
        "type": "block",
        "drop": [34],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [5],
        "required_tool_level": 0
    },
    35: {
        "name": "green flower",
        "breaking_time": 0.5,
        "txt": pygame.image.load("textures/blocks/kwiat6.png"),
        "type": "block",
        "drop": [35],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [5],
        "required_tool_level": 0
    },
    36: {
        "name": "red flower",
        "breaking_time": 0.5,
        "txt": pygame.image.load("textures/blocks/kwiat7.png"),
        "type": "block",
        "drop": [36],
        "amount": [1],
        "drop_probability": 1,
        "intended_tool": [5],
        "required_tool_level": 0
    },
    37: {
        "name": "wooden pickaxe",
        "txt": pygame.image.load("textures/items/wooden_pickaxe.png"),
        "type": "item",
        "tool_type": 1,
        "tool_level": 1,
        "crafting_recipe": [[[13,13,13],[0,23],[0,23]]],
        "crafting_amount": 1
    },
    38: {
        "name": "stone pickaxe",
        "txt": pygame.image.load("textures/items/stone_pickaxe.png"),
        "type": "item",
        "tool_type": 1,
        "tool_level": 2,
        "crafting_recipe": [[[5,5,5],[0,23],[0,23]]],
        "crafting_amount": 1
    },
    39: {
        "name": "iron pickaxe",
        "txt": pygame.image.load("textures/items/iron_pickaxe.png"),
        "type": "item",
        "tool_type": 1,
        "tool_level": 3,
        "crafting_recipe": [[[18,18,18],[0,23],[0,23]]],
        "crafting_amount": 1
    },
    40: {
        "name": "golden pickaxe",
        "txt": pygame.image.load("textures/items/golden_pickaxe.png"),
        "type": "item",
        "tool_type": 1,
        "tool_level": 2,
        "crafting_recipe": [[[17,17,17],[0,23],[0,23]]],
        "crafting_amount": 1
    },
    41: {
        "name": "diamond pickaxe",
        "txt": pygame.image.load("textures/items/diamond_pickaxe.png"),
        "type": "item",
        "tool_type": 1,
        "tool_level": 4,
        "crafting_recipe": [[[16,16,16],[0,23],[0,23]]],
        "crafting_amount": 1
    },
    42: {
        "name": "wooden axe",
        "txt": pygame.image.load("textures/items/wooden_axe.png"),
        "type": "item",
        "tool_type": 2,
        "tool_level": 1,
        "crafting_recipe": [[[13,13],[13,23],[0,23]],
                            [[13,13],[23,13],[23]]],
        "crafting_amount": 1
    },
    43: {
        "name": "stone axe",
        "txt": pygame.image.load("textures/items/stone_axe.png"),
        "type": "item",
        "tool_type": 2,
        "tool_level": 2,
        "crafting_recipe": [[[5,5],[5,23],[0,23]],
                            [[5,5],[23,5],[23]]],
        "crafting_amount": 1
    },
    44: {
        "name": "iron axe",
        "txt": pygame.image.load("textures/items/iron_axe.png"),
        "type": "item",
        "tool_type": 2,
        "tool_level": 3,
        "crafting_recipe": [[[18,18],[18,23],[0,23]],
                            [[18,18],[23,18],[23]]],
        "crafting_amount": 1
    },
    45: {
        "name": "golden axe",
        "txt": pygame.image.load("textures/items/golden_axe.png"),
        "type": "item",
        "tool_type": 2,
        "tool_level": 2,
        "crafting_recipe": [[[17,17],[17,23],[0,23]],
                            [[17,17],[23,17],[23]]],
        "crafting_amount": 1
    },
    46: {
        "name": "diamond axe",
        "txt": pygame.image.load("textures/items/diamond_axe.png"),
        "type": "item",
        "tool_type": 2,
        "tool_level": 4,
        "crafting_recipe": [[[16,16],[16,23],[0,23]],
                            [[16,16],[23,16],[23]]],
        "crafting_amount": 1
    },
    47: {
        "name": "wooden shovel",
        "txt": pygame.image.load("textures/items/wooden_shovel.png"),
        "type": "item",
        "tool_type": 3,
        "tool_level": 1,
        "crafting_recipe": [[[13],[23],[23]]],
        "crafting_amount": 1
    },
    48: {
        "name": "stone shovel",
        "txt": pygame.image.load("textures/items/stone_shovel.png"),
        "type": "item",
        "tool_type": 3,
        "tool_level": 2,
        "crafting_recipe": [[[5],[23],[23]]],
        "crafting_amount": 1
    },
    49: {
        "name": "iron shovel",
        "txt": pygame.image.load("textures/items/iron_shovel.png"),
        "type": "item",
        "tool_type": 3,
        "tool_level": 3,
        "crafting_recipe": [[[18],[23],[23]]],
        "crafting_amount": 1
    },
    50: {
        "name": "golden shovel",
        "txt": pygame.image.load("textures/items/golden_shovel.png"),
        "type": "item",
        "tool_type": 3,
        "tool_level": 2,
        "crafting_recipe": [[[17],[23],[23]]],
        "crafting_amount": 1
    },
    51: {
        "name": "diamond shovel",
        "txt": pygame.image.load("textures/items/diamond_shovel.png"),
        "type": "item",
        "tool_type": 3,
        "tool_level": 4,
        "crafting_recipe": [[[16],[23],[23]]],
        "crafting_amount": 1
    },
    # Miejsce na miecz i motykę
    61: {
        "name": "coal block",
        "breaking_time": 2,
        "txt": pygame.image.load("textures/blocks/coal_block.png"),
        "type": "block",
        "drop": [61],
        "amount": [1],
        "drop_probability": 1,
        "crafting_recipe": [[[19,19,19],[19,19,19],[19,19,19]]],
        "crafting_amount": 1,
        "intended_tool": [1],
        "required_tool_level": 1
    },
    62: {
        "name": "iron block",
        "breaking_time": 2,
        "txt": pygame.image.load("textures/blocks/iron_block.png"),
        "type": "block",
        "drop": [62],
        "amount": [1],
        "drop_probability": 1,
        "crafting_recipe": [[[18,18,18],[18,18,18],[18,18,18]]],
        "crafting_amount": 1,
        "intended_tool": [1],
        "required_tool_level": 1
    },
    63: {
        "name": "gold block",
        "breaking_time": 2,
        "txt": pygame.image.load("textures/blocks/gold_block.png"),
        "type": "block",
        "drop": [63],
        "amount": [1],
        "drop_probability": 1,
        "crafting_recipe": [[[17,17,17],[17,17,17],[17,17,17]]],
        "crafting_amount": 1,
        "intended_tool": [1],
        "required_tool_level": 1
    },
    64: {
        "name": "diamond block",
        "breaking_time": 2,
        "txt": pygame.image.load("textures/blocks/diamond_block.png"),
        "type": "block",
        "drop": [64],
        "amount": [1],
        "drop_probability": 1,
        "crafting_recipe": [[[16,16,16],[16,16,16],[16,16,16]]],
        "crafting_amount": 1,
        "intended_tool": [1],
        "required_tool_level": 1
    },
    65: {
        "name": "lapis block",
        "breaking_time": 2,
        "txt": pygame.image.load("textures/blocks/lapis_block.png"),
        "type": "block",
        "drop": [65],
        "amount": [1],
        "drop_probability": 1,
        "crafting_recipe": [[[20,20,20],[20,20,20],[20,20,20]]],
        "crafting_amount": 1,
        "intended_tool": [1],
        "required_tool_level": 1
    }


}
