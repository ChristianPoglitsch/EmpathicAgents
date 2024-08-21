import json
import os
from typing import Union 

from LLM_Character.communication.incoming_messages import LocationData 
from LLM_Character.util import check_if_file_exists

class MemoryTree: 
    def __init__(self): 
        self.tree = {}
    
    def load_from_file(self, f_saved):
        if check_if_file_exists(f_saved): 
            tree = json.load(open(f_saved))
            self.tree = tree
    
    def load_from_data(self, data:LocationData):
        self.update(data)

    def update(self, data:LocationData):
        self.tree[data.world] = {}
        for s in data.sectors:
            self.tree[data.world][s.sector] = {}
            for a in s.arenas:
                self.tree[data.world][s.sector][a.arena] = []
                for o in a.gameobjects:
                    self.tree[data.world][s.sector][a.arena] += [o.gameobject]

    def save(self, out_json):
        os.makedirs(os.path.dirname(out_json), exist_ok=True)
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


if __name__ == '__main__':
    f = f"..\..\storage\initial\personas\Isabella\spatial_memory.json"
    x = MemoryTree(f)

    # print(x.get_str_accessible_sector_arenas("dolores double studio:double studio"))
    print(x.get_str_accessible_sectors("Kortrijk"))
    print(x.get_str_accessible_sector_arenas("Kortrijk","Beguinage of Courtrai"))
    print(x.get_str_accessible_arena_game_objects("Kortrijk", "Beguinage of Courtrai", "supply store"))
