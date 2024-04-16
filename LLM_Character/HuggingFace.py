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


# Send and received data
class AiDataClass():
    def __init__(self, _value, _message):
        self._value = _value
        self._message = _message

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    

class HuggingFace:

    def __init__(self):
        self._model = None
        self._tokenizer = None


    def Init(self, model_id):
        self._model, self._tokenizer = self.LoadModel(model_id)
        

    def Query(self, message):
        return self.HuggingFaceQuery(self._model, self._tokenizer, message)


    def QuerySummarize(self):
        self.RunSummarizeHuggingFaceTransformers(self._model, self._tokenizer)


    def RunChatHuggingFaceCtransformers(self):

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


    def LoadModel(self, model_id):
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, load_in_4bit=True) #, device_map="auto") # device_map="auto",
        model.config.sliding_window = 4096
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        #tokenizer.bos_token = "<bos>"
        #tokenizer.pad_token = "<pad>"
        tokenizer.cls_token = "<cls>"
        tokenizer.sep_token = "<s>"
        tokenizer.mask_token = "<mask>"
        return model, tokenizer


    def RunSummarizeHuggingFaceTransformers(self, model, tokenizer):
    
        messages = MessagesAI()
        messages = messages.read_messages_from_json("messages.json")
    
        user_message = messages.get_user_message()
        message = MessageAI("Summerize the chat: " + user_message.get_user_message(), "user")
        messages = MessagesAI()
        messages.add_message(message)
        messages = self.HuggingFaceQuery(model, tokenizer, messages)


    def HuggingFaceQuery(self, model, tokenizer, messages):
        response = self.HuggingFaceTransformersQuery(model, tokenizer, messages)
        response = self.HuggingFaceTransformersDecodeMessage(response)
        message = MessageAI(response, "assistant")
        messages.add_message(message)
        print('--- ---\n ' + response + '\n--- ---')
        return messages, response


    def HuggingFaceTransformersQuery(self, model, tokenizer, messages):
        startTime = time.process_time()
        device = "cuda"
        inputs = tokenizer.apply_chat_template(messages.get_messages_formatted(), return_tensors="pt").to(device)  # tokenize=False)

        generation_config = GenerationConfig(
            do_sample=True,
            temperature=0.2, #1.0
            pad_token_id=tokenizer.eos_token_id,
            max_new_tokens=128
            )
        generation_config.eos_token_id = tokenizer.eos_token_id

        outputs = model.generate(inputs, generation_config=generation_config)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
        print('Processing time: ' + str(time.process_time() - startTime) + ' sec')
        return response


    def HuggingFaceTransformersDecodeMessage(self, message):
        #print(message)
        response = message.replace("[/INST]","[INST]").split("[INST]")
        #response = message.replace("GPT4 Correct Assistant:","GPT4 Corrent User:").split("GPT4 Corrent User:")
        return response[len(response)-1]
