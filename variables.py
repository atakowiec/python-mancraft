import pygame

entity_types = [
    # [name, maxhp, left_image, right_image, size]
    ["Pig", 10, pygame.image.load("textures/entity/pig_left.png"), pygame.image.load("textures/entity/pig_right.png"), (50, 30)],
]

fuel_list = {
    6: 400
}

furnace_recipes = {
    13: 14
}
