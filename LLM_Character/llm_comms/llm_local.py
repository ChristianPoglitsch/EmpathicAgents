from LLM_Character.llm_comms.llm_abstract import LLMComms
from LLM_Character.finetuning.models import load_base_model
from LLM_Character.messages_dataclass import AIMessages, AIMessage

from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, AutoModel
from sentence_transformers import SentenceTransformer
from transformers import PreTrainedTokenizer, PreTrainedModel
from transformers import BitsAndBytesConfig
from openai.types import Embedding
from peft import  PeftModel

import torch
import torch.nn.functional as F
from torch import Tensor

import time
import os

from typing import List, Optional, Union

# in order to prevent the terminal to be cluttered from all the torch/transformers warnings. 
import warnings
import logging

warnings.filterwarnings('ignore')
logging.getLogger('transformers').setLevel(logging.ERROR)


class LocalComms(LLMComms):
    """
    class responsible for sending messages to LocalLLM's.
    In short, a wrapper class for HuggingFace API. 
    """

    def __init__(self):
        self._model:PreTrainedModel = None    
        self._tokenizer:PreTrainedTokenizer = None
        self._embedding_model: SentenceTransformer = None

        self.max_tokens=100 
        self.temperature=0.8 
        self.top_p=1

    def init(self, base_model_id:str, finetuned_model_id:str=None):
        """
        Initialize the model and tokenizer using the specified model ID.
        If the model ID refers to a local fine tuned model, 
        then it will prioritize that over a model on huggingFace.
        """

        # FIXME: check if the model id's are valid before laoding them. 
        # or use try catch when loading them. 
        # especially for semantic comparason, you have to check if the model is made for that. 
        # the same can be done for chatting, checking if the model is a text generator type. 

        if finetuned_model_id:
            self._model, self._tokenizer = self._load_model_loc(base_model_id, finetuned_model_id)    
        else: 
            self._model, self._tokenizer = self._load_model_hf(base_model_id)
            
        #FIXME: change model !! cannot use mistral. 
        self._embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        

       
    def send_text(self, prompt:AIMessages, max_length=100) -> Optional[str]:
        """
        send a prompt to openAI endpoint for chat completions.
        """
        if len(prompt) == 0:
            return None
        
        response = self._request(self._model, self._tokenizer, prompt, max_length)
        response_decoded = self._decode_request(response)

        return response_decoded

    def send_embedding(self, keywords:str) -> Optional[List[Embedding]]:
        """send a prompt to openAI endpoint for embeddings.

        Args:
            keywords (str): keywords for which you convert it to embeddings.

        Returns:
            List[float]: The embedding vector, which is a list of floats.
            The length of vector depends on the model as listed in the
            [embedding guide](https://platform.openai.com/docs/guides/embeddings).
        """
        if len(keywords) == 0:
            return None
        return self._requese_emb(keywords)
    
    # FIXME: change parameters to dictionary via args or kwargs or whatever. 
    # there will be parameters present in a certain model that will not be in another model etc. 
    # see huggingface. 
    def set_params(self, max_tokens:int, temperature:int, top_p:int, amount_responses:int, max_retry_attemps:int, presence_penalty=None, frequency_penalty=None):

        if not self._validate_inputs(max_tokens, temperature, top_p, amount_responses, max_retry_attemps,  presence_penalty, frequency_penalty):
            return None

        self.max_tokens=max_tokens
        self.temperature=temperature 
        self.top_p=top_p  
        self.n= amount_responses
        self.max_retry_attempts=max_retry_attemps
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty

    # ---------
    #  PRIVATE
    # ---------

    # FIXME: should be changed, validate the parameters via Huggingface API of the model. 
    # certain models will have diferent parameters limits. 
    def _validate_inputs(self, max_tokens, temperature, top_p, n, max_retry_attemps, presence_penalty, frequency_penalty):
        b1 = max_tokens > 0 
        b2 = temperature >=0 and  temperature <=2
        b3 = top_p >= 0 and top_p <= 1
        b4 = n >= 1 and n <= 128
        b5 = max_retry_attemps >= 0
        b6 = presence_penalty or ( presence_penalty >= -2 and presence_penalty <= 2)
        b7 = frequency_penalty or ( frequency_penalty >= -2 and frequency_penalty <= 2)

        if all[b1,b2,b3,b4,b5,b6,b7] :
            return True
        return False
    
    def _check_local(self, finetuned_model_id):
        return os.path.isdir(f"trained\{finetuned_model_id}")
        
    # FIXME: 
    # this function should maybe be placed in models.py in finetuning, 
    # some refactoring/ restructuring may be needed. 
    def _load_model_loc(self, model_id:str, finetuned_model_id) -> tuple[PreTrainedModel,  PreTrainedTokenizer]:
        base_model = load_base_model(model_id)
        path = f"trained\{finetuned_model_id}"
        model = PeftModel.from_pretrained(base_model, path)
        tokenizer = AutoTokenizer.from_pretrained(model_id, padding_side="right", use_fast=False)
        return model, tokenizer


    def _load_model_hf(self, model_id:str) -> tuple[PreTrainedModel,  PreTrainedTokenizer]:
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
    
    def _request(self, 
                model: PreTrainedModel, 
                tokenizer:PreTrainedTokenizer, 
                message:Union[AIMessages, AIMessage],
                max_length:int) -> str:
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
        inputs = tokenizer.apply_chat_template(message.get_formatted(), return_tensors="pt").to(device)  # tokenize=False)

        generation_config = GenerationConfig(
            do_sample=True,
            temperature= 0.2, #1.0
            pad_token_id= tokenizer.eos_token_id,
            max_new_tokens= max_length
            )
        generation_config.eos_token_id = tokenizer.eos_token_id

        outputs = model.generate(inputs, generation_config=generation_config)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
        print('Processing time: ' + str(time.process_time() - startTime) + ' sec')
        return response

    def _decode_request(self, message:str) -> str:
        """
        Decode the response message from the model.

        Example:
            Given a raw response message:
            "[INST] nice [/INST] indeed [INST] nice [/INST] indeed [INST] nice [/INST] indeed"
            It will return:
            " indeed"
        """
        response = message.replace("[/INST]","[INST]").split("[INST]")
        return response[len(response)-1]
    

# FIXME: something completly different. 
# source : https://huggingface.co/tasks/feature-extraction
# https://huggingface.co/tasks/sentence-similarity

# What is Sentence Similarity?
# Sentence Similarity is a task that, given a source sentence and a set of target sentences, calculates how similar the target sentences are to the source.

# Sentence similarity models convert input text, like “Hello”, into vectors (called embeddings)
# that capture semantic information. We call this step to embed. Then, we calculate how close (similar) they are using cosine similarity.
# -> exactly what the paper 'generative agents' did. 


# https://stackoverflow.com/questions/60492839/how-to-compare-sentence-similarities-using-embeddings-from-bert
# FIXME: You should NOT use BERT's output as sentence embeddings for semantic similarity. 
# otherwise in init, give model id for a model specifically or semtnatic comparason? 

# TODO: convert output to Optional[List[Embedding]]  !!!

    def _requese_emb(self, keywords: str) -> Tensor:
        embeddings = self._embedding_model.encode(keywords, convert_to_tensor=True)
        return embeddings.cpu().tolist()
        # return embeddings
# 
#         OR
# 
#         # ibr: with this method, you can also use mistral, but it isnt recommended ig? 

#         # Without sentence-transformers, 
#         # you can use the model like this: 
#         # First, you pass your input through the transformer model, 
#         # then you have to apply the right pooling-operation on-top of the contextualized word embeddings.

#         #Mean Pooling - Take attention mask into account for correct averaging
#         def mean_pooling(model_output, attention_mask):
#             token_embeddings = model_output[0] #First element of model_output contains all token embeddings
#             input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
#             return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


#         # Sentences we want sentence embeddings for
#         sentences = ['This is an example sentence', 'Each sentence is converted']

#         # Load model from HuggingFace Hub
#         tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
#         model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

#         # Tokenize sentences
#         encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

#         # Compute token embeddings
#         with torch.no_grad():
#             model_output = model(**encoded_input)

#         # Perform pooling
#         sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

#         # Normalize embeddings
#         sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

#         print("Sentence embeddings:")
#         print(sentence_embeddings)



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
    else :
        print("DAS IST EINE KOLOSALE KONSPIRAZION  ~Luis de Funes")


