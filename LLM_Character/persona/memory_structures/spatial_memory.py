import json
import os 

class MemoryTree: 
    def __init__(self, f_saved): 
        self.tree = {}
        if check_if_file_exists(f_saved): 
            self.tree = json.load(open(f_saved))

    def save(self, out_json):
        with open(out_json, "w") as outfile:
            json.dump(self.tree, outfile) 

           
    def get_str_accessible_sectors(self ,world:str):
        return []

    def get_str_accessible_sector_arenas(self, world:str, sector:str|None):
        return []

    def get_str_accessible_arena_game_objects(self, world:str, sector:str|None, arena:str|None):
        return []

def check_if_file_exists(curr_file): 
    """
    Checks if a file exists
    ARGS:
    curr_file: path to the current csv file. 
    RETURNS: 
    True if the file exists
    False if the file does not exist
    """
    return os.path.isfile(curr_file) 

if __name__ == '__main__':
    f = f"..\..\storage\initial\personas\Isabella\spatial_memory.json"
    x = MemoryTree(f)

    # print(x.get_str_accessible_sector_arenas("dolores double studio:double studio"))
    print(x.get_str_accessible_sectors("Kortrijk"))
    print(x.get_str_accessible_sector_arenas("Kortrijk","Beguinage of Courtrai"))
    print(x.get_str_accessible_arena_game_objects("Kortrijk", "Beguinage of Courtrai", "supply store"))
