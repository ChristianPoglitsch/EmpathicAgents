# Created by Christian Poglitsch
#
#

from HuggingFace import HuggingFace
from gpt4all import GPT4All

import openai
import time
import torch
import os
import json
import time

from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

from UdpComms import UdpComms
from MessagesAI import MessagesAI, MessageAI
from Dataclasses import PromptMessage
from cognitive_modules.summary import summary



def RunServer(model:AutoModelForCausalLM, sock:UdpComms, messages:MessagesAI):

    while True:
    
        sendData = False
        dataclass = PromptMessage
        messages = messages.read_messages_from_json("messages.json")
        
        #sock.SendData('Sent from Python: ' + str(i)) # Send this string to other application

        data = sock.ReadReceivedData() # read data

        if data != None: # if NEW data has been received since last ReadReceivedData function call
  
            j = json.loads(data)
            dataclass = PromptMessage(**j)
            dataclass._value = dataclass._value + 1
            sendData = True
            print(dataclass._value)
    
        if sendData:
            # Reload if necessary            
            if dataclass._message == 'n':
                print("--- reset chat ---")
                messages = messages.read_messages_from_json("background.json")
            else:
                messages.add_message(messages.create_message(dataclass._message, "user"))
                messages, response = model.Query(messages)
                dataclass._message = response
                obj = json.dumps(dataclass.__dict__)
                sock.SendData(obj)
            sendData = False

        time.sleep(1)


def RunChat():

    model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf", n_threads=19, device='gpu')
    #model = GPT4All("mistral-7b-v0.1.Q3_K_M.gguf", n_threads=19, device='gpu')

    while True:
        message = input("Message: ")
        Speech(model, message)


def RunChatHuggingFaceCtransformers():

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
    print(tokenizer.decode(tokenized_chat[0]))

    outputs = model.generate(tokenized_chat, max_new_tokens=128) 
    print(tokenizer.decode(outputs[0]))

#FIXME: change function name due to method overloading not being supported in python.
def RunChatargs(model, messages):

    #messages = [
    #    {"role": "user", "content": "What is your favourite condiment?"},
    #    {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
    #    {"role": "user", "content": "Do you have mayonnaise recipes?"}
    #]

    load_initial = False

    if load_initial:

        #m1 = MessageAI("You are Camila. In this role you play a young woman living in Graz.\n " +
        #               "What you as Camila do: You like gardening. You do gardening in the morning, study in the afternoon Game Development and you go for some drinks in the evening.\n " +
        #               "Currently you are in Graz and the time is 11:00 AM.\n " +
        #               "This is what you like to find out about me:\n " + 
        #               "Background: My name, my age, where I live, where I work and my hobbies.\n " + 
        #               "Try to ask me as much as possible to find out more about me.\n " + 
        #               "Do not mention that you are an AI model. That would hurt the game. You have to stay in your role. Do not repeat yourself. Try to anwser with one sentence and one question. ", "user", class_type='Introduction') # Role of LLM agent"
        #m2 = MessageAI("Hello", "assistant")
        #messages.add_message(m1)
        #messages.add_message(m2)
    
        #messages.write_messages_to_json("messages.json")
        # load background story for agent
        messages = messages.read_messages_from_json("background.json")  
    else:
        messages = messages.read_messages_from_json("messages.json")

    chat_active = True
    while chat_active:
        message = input("Message: ")
        if message == 'q':
            break
        elif message == 's':
            print(messages.prints_messages())
        elif message == 'n':
            print("--- reset chat ---")
            messages = messages.read_messages_from_json("background.json")
        elif message == 'r':
            print("--- reload chat ---")
            messages = messages.read_messages_from_json("messages.json")           
        else:
            messages.add_message(messages.create_message(message, "user"))
            messages, _ = model.Query(messages)
            messages.write_messages_to_json("messages.json")

    print('...')


# Start main program
# Set HF_HOME for cache folder

# CUDA recommended!
print("CUDA found " + str(torch.cuda.is_available()))

messages = MessagesAI()

# Load Llama 3
#import transformers
#model_id = "meta-llama/Meta-Llama-3-8B"
#pipeline = transformers.pipeline("text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto", token=os.getenv("HF_TOKEN"))
#pipeline("Hey how are you doing today?")



# mistralai/Mixtral-8x7B-Instruct-v0.1 
# google/gemma-7b
# mistralai/Mistral-7B-Instruct-v0.2
model_id = "mistralai/Mistral-7B-Instruct-v0.2"
#model, tokenizer = LoadModel(model_id)
model = HuggingFace()
model.Init(model_id)

# Create UDP socket to use for sending (and receiving)
sock = UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)
#RunServer(model, sock, messages)

#RunChat()

# #FIXME: OSError: TheBloke/Mistral-7B-OpenOrca-GGUF does not appear to have a file named pytorch_model.bin, model.safetensors, tf_model.h5, model.ckpt or flax_model.msgpack.
# RunChatHuggingFaceCtransformers()

RunChatargs(model, messages)
summary(model)
