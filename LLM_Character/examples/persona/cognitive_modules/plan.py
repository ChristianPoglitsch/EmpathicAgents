import logging

from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.llm_comms.llm_local import LocalComms
from LLM_Character.llm_comms.llm_openai import OpenAIComms
from LLM_Character.persona.cognitive_modules import plan
from LLM_Character.persona.persona import Persona
from LLM_Character.util import BASE_DIR, LOGGER_NAME, setup_logging


def run_example_plan(person: Persona, verbose=False):
    scr = person.scratch
    a = scr.get_f_daily_schedule_index()
    assert a == 0
    b = scr.get_f_daily_schedule_hourly_org_index()
    assert b == 0
    c = scr.get_str_iss()
    assert isinstance(c, str)
    d = scr.get_curr_event()
    assert isinstance(d, None)
    e = scr.get_curr_event_and_desc()
    assert isinstance(e, None)
    f = scr.act_check_finished()
    assert isinstance(f, True)
    g = scr.act_summary_str()
    assert isinstance(g, str)
    h = scr.get_str_daily_schedule_summary()
    assert isinstance(h, str)
    i = scr.get_str_daily_schedule_hourly_org_summary()
    assert isinstance(i, str)

    if verbose:
        logger.info(f"Planning information of the person {scr.name}")
        logger.info(a)
        logger.info(b)
        logger.info(c)
        logger.info(d)
        logger.info(e)
        logger.info(f)
        logger.info(g)
        logger.info(h)
        logger.info(i)


if __name__ == "__main__":
    setup_logging("examples_reflect")
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("starting take off ...")

    modelb = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    modelb.init(model_id)

    modela = OpenAIComms()
    model_id = "gpt-4"
    modela.init(model_id)

    for model in modela, modelb:
        wrapper_model = LLM_API(model)

        person = Persona("Camila")
        person.load_from_file(
            BASE_DIR + "/LLM_Character/storage/initial/personas/Camila"
        )

        plan(person.scratch, person.a_mem,
             person.s_mem, "First Day", wrapper_model)
        run_example_plan(person)

        person = Persona("Camila")
        person.load_from_file(
            BASE_DIR + "/LLM_Character/storage/initial/personas/Camila"
        )

        plan(person.scratch, person.a_mem,
             person.s_mem, "New Day", wrapper_model)
        run_example_plan(person)

        person = Persona("Camila")
        person.load_from_file(
            BASE_DIR + "/LLM_Character/storage/initial/personas/Camila"
        )

        plan(person.scratch, person.a_mem, person.s_mem, None, wrapper_model)
        run_example_plan(person)

        person = Persona("Camila")
        person.load_from_file(
            BASE_DIR + "/LLM_Character/storage/initial/personas/Camila"
        )

        plan(person.scratch, person.a_mem,
             person.s_mem, "First Day", wrapper_model)
        plan(person.scratch, person.a_mem,
             person.s_mem, "New Day", wrapper_model)
        plan(person.scratch, person.a_mem, person.s_mem, None, wrapper_model)
        run_example_plan(person, True)
