import logging

from LLM_Character.communication.incoming_messages import OneLocationData
from LLM_Character.persona.memory_structures.spatial_memory import MemoryTree
from LLM_Character.util import BASE_DIR, LOGGER_NAME, setup_logging

if __name__ == "__main__":
    setup_logging("examples_associative_memory")
    logger = logging.getLogger(LOGGER_NAME)

    memory_tree = MemoryTree()
    memory_tree.load_from_file(
        BASE_DIR
        + "/LLM_Character/storage/localhost/default/personas/Florian/associative_memory"
    )

    location_data = OneLocationData(world="World3", sector="City3", arena="Arena1")
    memory_tree.update_oloc(location_data)

    memory_tree.save(
        BASE_DIR
        + "/LLM_Character/examples/persona/\
        memory_structures/temp/Florian/spatial_mem1.json"
    )

    info = memory_tree.get_info()
    logger.info("Memory Tree Data:", info)

    accessible_sectors = memory_tree.get_str_accessible_sectors("World1")
    logger.info("Accessible Sectors in World1:", accessible_sectors)

    accessible_arenas = memory_tree.get_str_accessible_sector_arenas("World1", "City1")
    logger.info("Accessible Arenas in City1 of World1:", accessible_arenas)

    accessible_game_objects = memory_tree.get_str_accessible_arena_game_objects(
        "World1", "City1", "Location1"
    )
    logger.info(
        "Accessible Game Objects in Location1 of City1 in World1:",
        accessible_game_objects,
    )

    memory_tree = MemoryTree()
    data = {
        "World1": {
            "City1": {"Location1": ["Detail1", "Detail2"], "Location2": ["Detail3"]},
            "City2": {"Location1": ["Detail4"]},
        },
        "World2": {"City1": {"Location1": ["Detail5"]}},
    }
    memory_tree.load_from_data(data)

    location_data = OneLocationData(world="World3", sector="City3", arena="Arena1")
    memory_tree.update_oloc(location_data)

    memory_tree.save(
        BASE_DIR
        + "/LLM_Character/examples/persona/\
        memory_structures/temp/Florian/spatial_mem1.json"
    )

    info = memory_tree.get_info()
    logger.info("Memory Tree Data:", info)

    accessible_sectors = memory_tree.get_str_accessible_sectors("World1")
    logger.info("Accessible Sectors in World1:", accessible_sectors)

    accessible_arenas = memory_tree.get_str_accessible_sector_arenas("World1", "City1")
    logger.info("Accessible Arenas in City1 of World1:", accessible_arenas)

    accessible_game_objects = memory_tree.get_str_accessible_arena_game_objects(
        "World1", "City1", "Location1"
    )
    logger.info(
        "Accessible Game Objects in Location1 of City1 in World1:",
        accessible_game_objects,
    )
