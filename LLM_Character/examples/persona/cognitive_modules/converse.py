if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_openai import OpenAIComms
    from LLM_Character.persona.persona import Persona
    from LLM_Character.persona.user import User
    from LLM_Character.util import BASE_DIR

    print("starting take off ...")

    # person = Persona("Camila", BASE_DIR + "/LLM_Character/storage/initial/personas/Camila")
    person = Persona(
        "Florian",
        BASE_DIR + "/LLM_Character/storage/localhost/default/personas/Florian",
    )
    user = User("Louis")

    # modelc = LocalComms()
    # model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    # modelc.init(model_id)

    modelc = OpenAIComms()
    model_id = "gpt-4"
    modelc.init(model_id)

    model = LLM_API(modelc)
    message = "hi"
    response = chatting(user.scratch, person.scratch, person.a_mem, message, model)
    # print("message")
    # print(message)
    # print("response")
    # print(response)

    message = "IM TERRIBLE, dont talk to me pls"
    response = chatting(user.scratch, person.scratch, person.a_mem, message, model)
    # print("message")
    # print(message)
    # print("response")
    # print(response)

    message = "i said stop talking, end this conversation, bye."
    response = chatting(user.scratch, person.scratch, person.a_mem, message, model)

    # print("message")
    # print(message)
    # print("response")
    # print(response)
