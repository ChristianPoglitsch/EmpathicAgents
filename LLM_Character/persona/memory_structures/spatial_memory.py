import json
import os 
from typing import Union 
from dataclasses import asdict
import sys
sys.path.append('../../')


from LLM_Character.world.validation_dataclass import LocationData, Sector, Arena, GameObject 

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

        memory_tree_instance = MemoryTree(f_saved)
        memory_tree_instance.tree = final_tree
        memory_tree_instance.save(f_saved)

    def save(self, out_json):
        with open(out_json, "w") as outfile:
            json.dump(self.tree, outfile) 
    
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


def check_if_file_exists(curr_file): 
    return os.path.isfile(curr_file) 

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
