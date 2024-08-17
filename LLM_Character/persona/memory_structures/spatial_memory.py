import json
from typing import Union 
import sys
sys.path.append('../../')

from LLM_Character.world.validation_dataclass import LocationData, Sector, Arena, GameObject 
from LLM_Character.util import check_if_file_exists

class MemoryTree: 
    def __init__(self, f_saved): 
        self.tree = {}
        if check_if_file_exists(f_saved): 
            self.tree = json.load(open(f_saved))

    @staticmethod
    def save_as(f_saved: str, data: LocationData):
        tree = {}

        for sector in data.sectors: 
            sector_tree = _process_sector(sector)
            tree[sector.sector] = sector_tree

        final_tree = {data.world: tree}

        with open(f_saved, "w") as outfile:
            json.dump(final_tree, outfile) 
    

    def save(self, out_json):
        with open(out_json, "w") as outfile:
            json.dump(self.tree, outfile) 
    
    def print_tree(self): 
        def _print_tree(tree, depth):
            dash = " >" * depth
            if type(tree) == type(list()): 
                if tree:
                    print (dash, tree)
                return 

            for key, val in tree.items(): 
                if key: 
                    print (dash, key)
                _print_tree(val, depth+1)
        
        _print_tree(self.tree, 0)
     
    def get_str_accessible_sectors(self ,world:str):
        return ", ".join(list(self.tree[world].keys()))
    
    def get_str_accessible_sector_arenas(self, world:str, sector:Union[str,None]):
        if not sector: 
          return ""
        return ", ".join(list(self.tree[world][sector].keys()))
    
    def get_str_accessible_arena_game_objects(self, world:str, sector:Union[str,None], arena:Union[str,None]):
        if not arena: 
          return ""
        try: 
          x = ", ".join(list(self.tree[world][sector][arena]))
        except: 
          x = ", ".join(list(self.tree[world][sector][arena.lower()]))
        return x

def _process_sector(sector: Sector) -> dict:
    sector_tree = {}
    for arena in sector.arenas or []:
        sector_tree[arena.arena] = _process_arena(arena)
    return sector_tree

def _process_arena(arena: Arena) -> list[str]:
    gameobject_list = [obj.gameobject for obj in (arena.gameobjects or [])]
    return gameobject_list

if __name__ == '__main__':
    f = f"..\..\storage\initial\personas\Isabella\spatial_memory.json"
    x = MemoryTree(f)

    # print(x.get_str_accessible_sector_arenas("dolores double studio:double studio"))
    print(x.get_str_accessible_sectors("Kortrijk"))
    print(x.get_str_accessible_sector_arenas("Kortrijk","Beguinage of Courtrai"))
    print(x.get_str_accessible_arena_game_objects("Kortrijk", "Beguinage of Courtrai", "supply store"))
