if __name__ == "__main__":
    x = LocalComms()
    #    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    x.init(model_id)
    # y = OpenAIComms()
    # model_id = "gpt-4"
    # y.init(model_id)

    hf = LLM_API(x)
    # hf = LLM_API(y)

    messages = AIMessages()
    m1 = AIMessage("Hello, how are you?", "user")
    m2 = AIMessage("I'm fine, thank you! How can I assist you today?", "assistant")
    m3 = AIMessage("Can you tell me a joke?", "user")
    m4 = AIMessage(
        "Why don't scientists trust atoms? Because they make up everything!",
        "assistant",
    )

    messages.add_message(m1)
    messages.add_message(m2)
    messages.add_message(m3)
    messages.add_message(m4)

    updated_messages, response = hf.query(messages)

    print("\n")
    print("--------------------------------")
    print("\n")

    print("Model response:")
    print(response)

    print("\n")
    print("--------------------------------")
    print("\n")

    print("\nUpdated messages:")
    # for message in updated_messages.get_messages_formatted():
    #     print(message)
    print(updated_messages.prints_messages())

    print("\n")
    print("--------------------------------")
    print("\n")

    summary, _ = hf.query_summary(updated_messages)
    print("\nChat summary:")
    print(summary.prints_messages())
