if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_openai import OpenAIComms
    from LLM_Character.persona.persona import Persona
    from LLM_Character.persona.user import User
    from LLM_Character.util import BASE_DIR

    print("starting take off ...")

    # person = Persona("Camila", BASE_DIR + "/LLM_Character/storage/initial/personas/Camila")
    person = Persona("Florian")
    person.load_from_file(
        BASE_DIR + "/LLM_Character/storage/localhost/default/personas/Florian"
    )
    user = User("Louis")

    modelc = OpenAIComms()
    model_id = "gpt-4"
    modelc.init(model_id)
    model = LLM_API(modelc)

    location_data = OneLocationData(
        world="Graz", sector="Saint Martin's Church", arena="cage", obj="refrigerator"
    )

    perceived_events = [
        EventData(
            action_event_subject="Graz:Saint Martin's Church:cafe:Florian",
            action_event_predicate="picked up",
            action_event_object="box",
            action_event_description="The robot picked up the box from the ground.",
        ),
        EventData(
            action_event_subject="Graz:Saint Martin's Church:cafe:Florian",
            action_event_predicate=None,
            action_event_object=None,
            action_event_description=None,
        ),
    ]

    events = perceive(
        person.scratch,
        person.a_mem,
        person.s_mem,
        location_data,
        perceived_events,
        model,
    )
