""" This module provides a class `HuggingFace` for interacting with Hugging Face models. It also manages GPT models. """ 

import time
from dataclass import AIMessages, AIMessage
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from transformers import PreTrainedTokenizer, PreTrainedModel
from transformers import BitsAndBytesConfig
import torch

# in order to prevent the terminal to be cluttered from all the torch/transformers warnings. 
import warnings
import logging

warnings.filterwarnings('ignore')
logging.getLogger('transformers').setLevel(logging.ERROR)

class HuggingFace():
    """
    A class to handle operations related to Hugging Face models, 
    including loading models, querying models, and summarizing messages.
    """
    def __init__(self):
        self._model = None
        self._tokenizer = None

    def init(self, model_id:str, max_length:int):
        """
        Initialize the model and tokenizer using the specified model ID.
        
        Args:
            model_id (str): The identifier for the model to load.
            max_length (int): the maximum amount of new tokens.
        """
        self._model, self._tokenizer = self._load_model(model_id)
        self.max_length = max_length

    def query(self, message:AIMessages) -> tuple[AIMessages, str]:
        """
        Query the model with a given chat.
        
        Returns:
            tuple: A tuple containing the updated messages and the model's response.
        """
        return self._huggingface_query(self._model, self._tokenizer, message)

    def query_summary(self, chat:AIMessages) -> AIMessages:
        """
        Summarize the chat using the loaded model and tokenizer.
        """
        return self._run_summarize_huggingface_transformers(self._model, self._tokenizer, chat)


    # -------------
    # Private
    # -------------

    def _load_model(self, model_id:str) -> tuple[PreTrainedModel,  PreTrainedTokenizer]:
        """
        Load the model and tokenizer from the specified model ID.
        
        Returns:
            tuple: A tuple containing the model and tokenizer.
        """

        # The `load_in_4bit` and `load_in_8bit` arguments are deprecated and will be removed in the future versions. 
        # Please, pass a `BitsAndBytesConfig` object in `quantization_config` argument instead.
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True
        )

        model = AutoModelForCausalLM.from_pretrained( #device_map="auto"
            model_id,
            quantization_config=quantization_config,
            torch_dtype=torch.bfloat16
        )    
        model.config.sliding_window = 4096
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        # tokenizer.bos_token = "<bos>"
        # tokenizer.pad_token = "<pad>"
        tokenizer.cls_token = "<cls>"
        tokenizer.sep_token = "<s>"
        tokenizer.mask_token = "<mask>"
        return model, tokenizer


    # QUESTION: Why only summarise user messages of the chat?
    # see todo.md
    def _run_summarize_huggingface_transformers(self, model:PreTrainedModel, tokenizer:AutoTokenizer, messages:AIMessages) -> AIMessages:
        """
        Summarize the chat by reading messages from a JSON file and generating a summary.
        
        Args:
            model: The model to use for summarization.
            tokenizer: The tokenizer to use for summarization.
        
        Returns: 
            AIMessages: An instance of AIMessages with 2 messages with the last one being the summary. 
        """
        # loaded_messages = AIMessages.read_messages_from_json("messages.json")
        # user_messages_concatenated = loaded_messages.get_user_message()
        user_messages_concatenated = messages.get_user_message()
        message = AIMessage("Summerize the chat: " + user_messages_concatenated.get_user_message(), "user") 
        
        messages = AIMessages()
        messages.add_message(message)
        messages, _ = self._huggingface_query(model, tokenizer, messages)
        
        return messages

    def _huggingface_query(self, model:PreTrainedModel, tokenizer:AutoTokenizer, messages:AIMessages) -> tuple[AIMessages, str]:
        """
        Generate a response from the model based on the provided messages.
        
        Args:
            model: The model to use for querying.
            tokenizer: The tokenizer to use for querying.
            messages: The messages to query the model with.
        
        Returns:
            tuple: A tuple containing the updated messages and the model's response.
        """
        response = self._huggingface_transformers_query(model, tokenizer, messages)
        response = self._huggingface_transformers_decode_message(response)
        message = AIMessage(response, "assistant")
        messages.add_message(message)
        # print('--- ---\n ' + response + '\n--- ---')
        return messages, response


    def _huggingface_transformers_query(self, 
                                        model: PreTrainedModel, 
                                        tokenizer:PreTrainedTokenizer, 
                                        messages:AIMessages) -> str:
        """
        Generate a response from the model based on the input messages.
        
        Args:
            model: The model to use for querying.
            tokenizer: The tokenizer to use for querying.
            messages: The messages to query the model with.
        
        Returns:
            str: The model's response.
        """
        startTime = time.process_time()
        
        device = "cuda"
        inputs = tokenizer.apply_chat_template(messages.get_messages_formatted(), return_tensors="pt").to(device)  # tokenize=False)

        generation_config = GenerationConfig(
            do_sample=True,
            temperature= 0.2, #1.0
            pad_token_id= tokenizer.eos_token_id,
            max_new_tokens= self.max_length
            )
        generation_config.eos_token_id = tokenizer.eos_token_id

        outputs = model.generate(inputs, generation_config=generation_config)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
        print('Processing time: ' + str(time.process_time() - startTime) + ' sec')
        return response

    def _huggingface_transformers_decode_message(self, message:str) -> str:
        """
        Decode the response message from the model.

        Example:
            Given a raw response message:
            "[INST] nice [/INST] indeed [INST] nice [/INST] indeed [INST] nice [/INST] indeed"
            It will return:
            " indeed"
        """
        response = message.replace("[/INST]","[INST]").split("[INST]")
        #response = message.replace("GPT4 Correct Assistant:","GPT4 Corrent User:").split("GPT4 Corrent User:")

        return response[len(response)-1]

if __name__ == "__main__":
    hf = HuggingFace()
    
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    hf.init(model_id)
    
    messages = AIMessages()
    m1 = AIMessage("Hello, how are you?", "user")
    m2 = AIMessage("I'm fine, thank you! How can I assist you today?", "assistant")
    m3 = AIMessage("Can you tell me a joke?", "user")
    m4 = AIMessage("Why don't scientists trust atoms? Because they make up everything!", "assistant")
    
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
    
    summary = hf.query_summary(updated_messages)
    print("\nChat summary:")
    print(summary.prints_messages())
