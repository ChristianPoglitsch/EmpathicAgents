import openai
import time
import torch
import os
import json
import time

from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer
from gpt4all import GPT4All

from udp_comms import UdpComms
from huggingface import HuggingFace
from speach import speech
from dataclass import AIMessages, PromptMessage
from cognitive_modules.summary import summary

def run_server(model:HuggingFace, sock:UdpComms, messages:AIMessages):
    messages = messages.read_messages_from_json("dialogues/messages.json") # --> previous messages.
    print("Running Server... \n")
    while True:
        byte_data = sock.ReadReceivedData() # non blocking read data
        if byte_data != None: # if NEW data has been received since last ReadReceivedData function call
            obj = json.loads(byte_data)
            pm = PromptMessage(**obj)
    
            # Reload if necessary            
            if pm._message == 'n':
                print("--- reset chat ---")
                messages = messages.read_messages_from_json("dialogues/background.json")
            else:
                messages.add_message(messages.create_message(pm._message, "user"))
                messages, response = model.query(messages)
                
                pm._value = pm._value + 1
                pm._message = response
                
                obj = json.dumps(pm.__dict__)
                sock.SendData(obj)
    
        time.sleep(1)

def run_interaction():
    model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf", n_threads=19, device='gpu')
    #model = GPT4All("mistral-7b-v0.1.Q3_K_M.gguf", n_threads=19, device='gpu')
    while True:
        message = input("Message: ")
        speech(model, message)

def run_template():
    # TODO: convert your downloaded weights to Hugging Face Transformers format 
    model = AutoModelForCausalLM.from_pretrained("TheBloke/Mistral-7B-OpenOrca-GGUF", model_file="mistral-7b-openorca.Q4_K_M.gguf", model_type="mistral", 
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
        {"role": "system", "content": "You are a friendly chatbot who always responds in the style of a pirate",},
        {"role": "user", "content": "How many helicopters can a human eat in one sitting?"},
    ]
    tokenized_chat = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt")
    # print(tokenizer.decode(tokenized_chat[0]))

    outputs = model.generate(tokenized_chat, max_new_tokens=128) 
    print(tokenizer.decode(outputs[0]))

def run_chat(model:HuggingFace):
    messages = AIMessages.read_messages_from_json("dialogues/messages.json")
    while True:
        message = input("Message: ")
        if message == 'q':
            break
        elif message == 's':
            print(messages.prints_messages())
        elif message == 'n':
            print("--- reset chat ---")
            messages = messages.read_messages_from_json("dialogues/background.json")
        elif message == 'r':
            print("--- reload chat ---")
            messages = messages.read_messages_from_json("dialogues/messages.json")           
        else:
            messages.add_message(messages.create_message(message, "user"))
            messages, response = model.query(messages)
            print(response.split('{"Message')[0])
            messages.write_messages_to_json("dialogues/messages.json")



if __name__ == "__main__":
    # Set HF_HOME for cache folder
    # CUDA recommended!
    print("CUDA found " + str(torch.cuda.is_available()))

    # model_id = "meta-llama/Meta-Llama-3-8B"
    # model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1" 
    # model_id = "google/gemma-7b"
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    model = HuggingFace()
    model.init(model_id)

    # Create UDP socket to use for sending (and receiving)
    sock = UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)
    messages = AIMessages()
    
    run_server(model, sock, messages)

    # run_chat(model)

    # run_interaction()

    # #FIXME: OSError: TheBloke/Mistral-7B-OpenOrca-GGUF does not appear to have a file named pytorch_model.bin, model.safetensors, tf_model.h5, model.ckpt or flax_model.msgpack.
    # run_template()

    # summary(model)
