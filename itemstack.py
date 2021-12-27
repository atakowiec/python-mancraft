from world import blocks as block_types


class ItemStack:
    def __init__(self, item_id, count=1):
        self.item_id = item_id
        self.name = block_types[item_id][0]
        self.txt = block_types[item_id][2]
        self.count = count
