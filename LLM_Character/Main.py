# Created by Christian Poglitsch
#
#

import UdpComms as U
import time
import openai
from gpt4all import GPT4All
import torch
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import azure.cognitiveservices.speech as speechsdk
import json
import time
from MessagesAI import MessagesAI, MessageAI


def SpeechVoice(model):
    print('Start SpeechRecognizer')
    language = 'en-US' # 'de-AT' 'en-US'
    speechConfig = speechsdk.SpeechConfig(subscription=os.getenv('AZURE_KEY'), region="westeurope", speech_recognition_language=language)

    speechConfig.speech_synthesis_voice_name= 'en-US-JennyNeural' #' 'de-AT-IngridNeural' 'en-US-JennyNeural'
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speechConfig, audio_config=audio_config)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speechConfig, audio_config=audio_config)

    speech_recognized = 'Hallo'

    print("Speak into your microphone.")
    speech_recognized = speech_recognizer.recognize_once()
    print(speech_recognized.text)
    #speech_synthesis_result = speech_synthesizer.speak_text_async(speech_recognized.text).get() #result.text
    print('Stop SpeechRecognizer')

    response = Speech(model, speech_recognized.text)
    speech_synthesis_result = speech_synthesizer.speak_text_async(response).get()

    print(response)
    print('Test finished')
    return response, speech_synthesis_result


def Speech(model, message):
    print('Start LLM processing')

    chat_history = ''
    system_template = 'Your role is to be an empathic agent. Your name is Camila. Get information about the user like name, age, gender and his or her live in general. '
    # many models use triple hash '###' for keywords, Vicunas are simpler:
    prompt_template = 'USER: {0}\nASSISTANT:'
    temperature = 0.7
    with model.chat_session(system_template, prompt_template):
        response = model.generate(prompt=message, temp=temperature)

    print(response)
    print('LLM processing finished')
    return response


# Send and received data
class AiDataClass():
    def __init__(self, _value, _message):
        self._value = _value
        self._message = _message

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


def RunServer(model, sock):

    while True:
    
        sendData = False
        dataclass = AiDataClass
        messages = MessagesAI()
        recent_messages = messages.read_messages_from_json("messages.json")
        for item in recent_messages.get_messages():
            messages.add_message(item)
        
        #sock.SendData('Sent from Python: ' + str(i)) # Send this string to other application

        data = sock.ReadReceivedData() # read data

        if data != None: # if NEW data has been received since last ReadReceivedData function call
  
            j = json.loads(data)
            dataclass = AiDataClass(**j)
            dataclass._value = dataclass._value + 1
            sendData = True
            print(dataclass._value)
    
        if sendData:
            # Reload if necessary            
            if dataclass._message == 'n':
                print("--- reset chat ---")
                messages = MessagesAI()
                recent_messages = messages.read_messages_from_json("messages.json")
                for item in recent_messages.get_messages():
                    messages.add_message(item)
            else:
                messages.add_message(MessageAI(dataclass._message, "user"))
                messages, response = HuggingFaceQuery(model, tokenizer, messages)
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


def LoadModel(model_id):
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, load_in_4bit=True) # device_map="auto",
    model.config.sliding_window = 4096
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    #tokenizer.bos_token = "<bos>"
    #tokenizer.pad_token = "<pad>"
    tokenizer.cls_token = "<cls>"
    tokenizer.sep_token = "<s>"
    tokenizer.mask_token = "<mask>"
    return model, tokenizer


def RunChatHuggingFaceTransformers(model, tokenizer):

    #messages = [
    #    {"role": "user", "content": "What is your favourite condiment?"},
    #    {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
    #    {"role": "user", "content": "Do you have mayonnaise recipes?"}
    #]

    load_initial = False
    messages = MessagesAI()

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
        recent_messages = messages.read_messages_from_json("messages.json")
        for item in recent_messages.get_messages():
            messages.add_message(item)

    chat_active = True
    while chat_active:
        message = input("Message: ")
        if message == 'q':
            break
        elif message == 's':
            print(messages.prints_messages())
        elif message == 'n':
            print("--- reset chat ---")
            messages = MessagesAI()
            recent_messages = messages.read_messages_from_json("background.json")
            for item in recent_messages.get_messages():
                messages.add_message(item)
        elif message == 'r':
            print("--- reload chat ---")
            messages = MessagesAI()
            recent_messages = messages.read_messages_from_json("messages.json")
            for item in recent_messages.get_messages():
                messages.add_message(item)                 
        else:
            message = MessageAI(message, "user")
            messages.add_message(message)
            messages, _ = HuggingFaceQuery(model, tokenizer, messages)
            messages.write_messages_to_json("messages.json")

    print('...')


def RunSummarizeHuggingFaceTransformers(model, tokenizer):
    
    messages = MessagesAI()
    messages = messages.read_messages_from_json("messages.json")
    
    user_message = messages.get_user_message()
    message = MessageAI("Summerize the chat: " + user_message.get_user_message(), "user")
    messages = MessagesAI()
    messages.add_message(message)
    messages = HuggingFaceQuery(model, tokenizer, messages)


def HuggingFaceQuery(model, tokenizer, messages):
    response = HuggingFaceTransformersQuery(model, tokenizer, messages)
    response = HuggingFaceTransformersDecodeMessage(response)
    message = MessageAI(response, "assistant")
    messages.add_message(message)
    print('--- ---\n ' + response + '\n--- ---')
    return messages, response


def HuggingFaceTransformersQuery(model, tokenizer, messages):
    startTime = time.process_time()
    device = "cuda"
    inputs = tokenizer.apply_chat_template(messages.get_messages_formatted(), return_tensors="pt").to(device)  # tokenize=False)

    generation_config = GenerationConfig(
        do_sample=True,
        temperature=1.0, #1.0
        pad_token_id=tokenizer.eos_token_id,
        max_new_tokens=150
        )
    generation_config.eos_token_id = tokenizer.eos_token_id

    outputs = model.generate(inputs, generation_config=generation_config)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print('Processing time: ' + str(time.process_time() - startTime) + ' sec')
    return response


def HuggingFaceTransformersDecodeMessage(message):
    #print(message)
    response = message.replace("[/INST]","[INST]").split("[INST]")
    #response = message.replace("GPT4 Correct Assistant:","GPT4 Corrent User:").split("GPT4 Corrent User:")
    return response[len(response)-1]


# Start main program
# Set HF_HOME for cache folder

# CUDA recommended!
print("CUDA found " + str(torch.cuda.is_available()))

model_id = "mistralai/Mistral-7B-Instruct-v0.2" # "mistralai/Mixtral-8x7B-Instruct-v0.1" # "mistralai/Mistral-7B-Instruct-v0.1" # mistralai/Mistral-7B-Instruct-v0.2 # openchat/openchat-3.5-0106
model, tokenizer = LoadModel(model_id)

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)
#RunServer(model, sock)

#RunChat()
#RunChatHuggingFaceCtransformers()

RunChatHuggingFaceTransformers(model, tokenizer)
RunSummarizeHuggingFaceTransformers(model, tokenizer)
