"""
Plan new steps or quests.
"""

from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.persona.memory_structures.spatial_memory import MemoryTree
from LLM_Character.persona.memory_structures.scratch.persona_scratch import PersonaScratch
from LLM_Character.persona.memory_structures.associative_memory.associative_memory import AssociativeMemory
from LLM_Character.persona.cognitive_modules.planning.long_term_planning import _long_term_planning
from LLM_Character.persona.cognitive_modules.planning.determine_action import _determine_action


def plan(
        scratch: PersonaScratch,
        a_mem: AssociativeMemory,
        s_mem: MemoryTree,
        new_day: str,
        model: LLM_API):
    if new_day:
        _long_term_planning(scratch, a_mem, new_day, model)

    if scratch.act_check_finished():
        _determine_action(scratch, s_mem, model)

    return scratch.act_address


if __name__ == "__main__":
    from LLM_Character.persona.persona import Persona
    from LLM_Character.llm_comms.llm_openai import OpenAIComms
    from LLM_Character.llm_comms.llm_local import LocalComms
    from LLM_Character.util import BASE_DIR

    print("starting take off ...")

    # modelc = LocalComms()
    # model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    # modelc.init(model_id)

    modelc = OpenAIComms()
    model_id = "gpt-4"
    modelc.init(model_id)

    model = LLM_API(modelc)

    def print_plan(person: Persona):
        scr = person.scratch
        x1 = scr.get_f_daily_schedule_index()
        x2 = scr.get_f_daily_schedule_hourly_org_index()
        x3 = scr.get_str_iss()
        x5 = scr.get_curr_event()
        x6 = scr.get_curr_event_and_desc()
        x8 = scr.act_check_finished()
        x10 = scr.act_summary_str()
        x11 = scr.get_str_daily_schedule_summary()
        x12 = scr.get_str_daily_schedule_hourly_org_summary()

        print(x1)
        print(x2)
        print(x3)
        print(x5)
        print(x6)
        print(x8)
        print(x10)
        print(x11)
        print(x12)
    # -----------
    person = Persona("Camila", BASE_DIR +
                     "/LLM_Character/storage/initial/personas/Camila")
    plan(person.scratch, person.a_mem, person.s_mem, "First Day", model)
    print(print_plan(person))
    # -----------
    # person = Persona("Camila", BASE_DIR + "/LLM_Character/storage/initial/personas/Camila")
    # plan(person.scratch, person.a_mem, person.s_mem, "New Day", model)
    # print(print_plan(person))
    # # -----------
    # person = Persona("Camila", BASE_DIR + "/LLM_Character/storage/initial/personas/Camila")
    # plan(person.scratch, person.a_mem, person.s_mem, None, model)
    # print(print_plan(person))

    # # -----------
    # person = Persona("Camila", BASE_DIR + "/LLM_Character/storage/initial/personas/Camila")
    # plan(person.scratch, person.a_mem, person.s_mem, "First Day", model)
    # plan(person.scratch, person.a_mem, person.s_mem, "New Day", model)
    # plan(person.scratch, person.a_mem, person.s_mem, None, model)
    # print(print_plan(person))
