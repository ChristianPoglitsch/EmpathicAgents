if __name__ == "__main__":
    x = OpenAIComms()
    model_id = "gpt-4"
    x.init(model_id)

    aimessages = AIMessages()
    aimessages.add_message(AIMessage("Hi", "assistant"))

    res = x.send_text(aimessages)
    res2 = x.send_embedding("inderdaad")

    if res and res2:
        print("Dit is mooi")
        print(res)
    else:
        print("DAS IST EINE KOLOSALE KONSPIRAZION  ~Luis de Funes")
