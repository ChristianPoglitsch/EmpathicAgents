"""
the game, where the infinite loop will be receive information
from the unity game engine. 
"""





def start_server():
    """
      The main backend server. 
    """

    # NOTE: for testing purposes, we will be reading from a file. 
    
    # sim_folder = f"{fs_storage}/{self.sim_code}"



    # basically, how i understand it, is that, the loop starts
    # the world is initialised
    # the persona makes a move 
    # the persona saves some stuff to memory 
    # the world gets updated based on the memory of the persona
    # and the loop continues. 

    # instead, the location of the persona, if it moves, 
    # it gets send to the unity engine
    # at every loop, the new position is geven back in order 
    # to update the world perception
    # but why does the world need to save the place of the persona? 
    # is it only in order to access the nearby events (from the nearby tiles)
    # in that case, unity can handle that .
    # unity sends only the relevant events. 
    # and sends the whole spatial information needed
    # and the persona keeps trakc of which location it visited. 


    





