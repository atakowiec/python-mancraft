from variables import block_type


class ItemStack:
    def __init__(self, item_id, count=1, behind=False):
        self.item_id = item_id
        self.name = block_type[item_id]["name"]
        self.txt = block_type[item_id]["txt"]
        self.type = block_type[item_id]["type"]
        self.data = block_type[item_id]
        self.count = count
        self.behind = behind
