if __name__ == "__main__":
    x = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    x.init(model_id)

    aimessages = AIMessages()
    aimessages.add_message(AIMessage("Hi", "user"))

    res = x.send_text(aimessages)
    res2 = x.send_embedding("inderdaad")

    print(res)
    print(res2)
    if res and res2 is not None:
        print("Dit is mooi")
    else:
        print("DAS IST EINE KOLOSALE KONSPIRAZION  ~Luis de Funes")
