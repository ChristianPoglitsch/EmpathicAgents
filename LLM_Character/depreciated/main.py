import openai
import time
import torch
import os
import json
import time

from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer
from gpt4all import GPT4All

from LLM_Character.communication_module.udp_comms import UdpComms
from LLM_Character.llm_comms.llm_api import LLM_API
from speach import speech
from messages_dataclass import AIMessages, PromptMessage
from persona.cognitive_modules.summary import summary


def run_server(model: LLM_API, sock: UdpComms, messages: AIMessages):
    # --> previous messages.
    messages = messages.read_messages_from_json("dialogues/messages.json")
    print("Running Server... \n")
    while True:
        byte_data = sock.ReadReceivedData()  # non blocking read data
        if byte_data is not None:  # if NEW data has been received since last ReadReceivedData function call
            obj = json.loads(byte_data)
            pm = PromptMessage(**obj)

            # messages, response = model.query_text(pm._message, messages)
            response = reverie(pm._message)
            pm._value = pm._value + 1
            pm._message = response

            obj = json.dumps(pm.__dict__)
            sock.SendData(obj)

        time.sleep(1)


def run_interaction():
    model = GPT4All(
        "mistral-7b-instruct-v0.1.Q4_0.gguf",
        n_threads=19,
        device='gpu')
    # model = GPT4All("mistral-7b-v0.1.Q3_K_M.gguf", n_threads=19, device='gpu')
    while True:
        message = input("Message: ")
        speech(model, message)


def run_template():
    # TODO: convert your downloaded weights to Hugging Face Transformers format
    model = AutoModelForCausalLM.from_pretrained(
        "TheBloke/Mistral-7B-OpenOrca-GGUF",
        model_file="mistral-7b-openorca.Q4_K_M.gguf",
        model_type="mistral",
        gpu_layers=50,
        hf=True,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1.2,
        context_length=8096,
        max_new_tokens=2048,
        threads=os.cpu_count() - 1)
    tokenizer = AutoTokenizer.from_pretrained(model)

    messages = [
        {"role": "system", "content": "You are a friendly chatbot who always responds in the style of a pirate", },
        {"role": "user", "content": "How many helicopters can a human eat in one sitting?"},
    ]
    tokenized_chat = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
    # print(tokenizer.decode(tokenized_chat[0]))

    outputs = model.generate(tokenized_chat, max_new_tokens=128)
    print(tokenizer.decode(outputs[0]))


def run_chat(model):
    messages = AIMessages.read_messages_from_json("dialogues/messages.json")
    while True:
        message = input("Message: ")
        if message == 'q':
            break
        elif message == 's':
            print(messages.prints_messages())
        elif message == 'n':
            print("--- reset chat ---")
            messages = messages.read_messages_from_json(
                "dialogues/background.json")
        elif message == 'r':
            print("--- reload chat ---")
            messages = messages.read_messages_from_json(
                "dialogues/messages.json")
        else:
            messages.add_message(messages.create_message(message, "user"))
            messages, response = model.query(messages)
            print(response.split('{"Message')[0])
            messages.write_messages_to_json("dialogues/messages.json")
