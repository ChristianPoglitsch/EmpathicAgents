"""
Similar to the maze.py file in the other repository. 

defines the world class, which represents the virtual world of the game. 
"""


# NOTE: we kunnen er ook voor zorgen dat, wanneer we de informatie ontvagen van de unity game engine over spatial location, 
# dat het ook de naburige andere NPC's ook meestuurt, dan kan dat gezien worden als een event. 
# en dan kan onze agent beslissen of het met die NPC wilt babbelen of niet. 
# Unity, kan eventueel ook andere dingen doorsturen over die andere NPC's zoals met welke gameobject in de hierarchie ze aan het interacheren zijn.
# en dan kunnne wij da omvormen naar een <ConceptNode> etc.

class World: 
    def __init__(self, world_name):
        # [SECTION1] READING THE BASIC META INFORMATION ABOUT THE WORLD MAP. 
        self.world_name = world_name

        # TODO: this json file, was written with another module, 
        # which interacts with the unity engine in order to retrieve
        # the necessary information.

        # Reading in the meta information about the world.
        meta_info = json_load(open(f"{env_matrix}world_meta_info.json"))

        # NOTE: sepcial_contraints, i dont think i need this? idk

        # [SECTION2] READING IN SPECIAL BLOCKS
        # game objects in the unity scene that are highlighted, 
        # in which you can interact in order to cause events.

        # uiteindelijk zouden we ook een lijst hebben van 
        # sector_world, arena_world, game_object_world. 


        # every game object, that being sent to the python endpoint, 
        # in order to interact, is stored in a dictionary, called
        # self.tiles ig ? :FIXME: 

        # it contain information about the world, sector, arena and game_object. 
        # is that needed though? information about the world, sector, arena, 
        # spwaning_location
        # in a free world environment ? i dont think so,  FIXME: 

        # the keys are the center of object/mass of the object, in xyz coordinates. 
        # those coordinates can be floats, so it could be the case 
        # to make it less precise, to convert it into int16 for example? idk

        # e.g., self.tiles[32][59] = {'world': 'double studio', 
        #            'sector': '', 'arena': '', 'game_object': '', 
        #            'spawning_location': '', 'collision': False, 'events': set()}
        # e.g., self.tiles[9][58] = {'world': 'double studio', 
        #         'sector': 'double studio', 'arena': 'bedroom 2', 
        #         'game_object': 'bed', 'spawning_location': 'bedroom-2-a', 
        #         'collision': False,
        #         'events': {('double studio:double studio:bedroom 2:bed',
        #                    None, None)}} 


        # maybe spawining_location could be usefull, but i dont think so. 
        # tile_details["events"] = set()

        # i dont think i need to store events ?
        # i think in unity, if you trigger something, send the name of the gameobejct, room, arena, sector and scene to this endpoint. 

        # Each game object occupies an event in the tile. We are setting up the 
        # default event value here. 
        for i in range(self.maze_height):
          for j in range(self.maze_width): 
            if self.tiles[i][j]["game_object"]:
              object_name = ":".join([self.tiles[i][j]["world"], 
                                      self.tiles[i][j]["sector"], 
                                      self.tiles[i][j]["arena"], 
                                      self.tiles[i][j]["game_object"]])
              go_event = (object_name, None, None, None)
              self.tiles[i][j]["events"].add(go_event)
















