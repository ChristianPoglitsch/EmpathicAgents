""" inspired by 
https://github.com/adimis-ai/Large-Language-Model-LLM-Wrapper-from-Scratch-using-Openai-models/blob/main/Large_Language_Model_(LLM)_Wrapper_from_Scratch_using_Openai_models.ipynb
https://github.com/openai/openai-python
https://github.com/joonspk-research/generative_agents
"""

from openai import OpenAI 
from dataclass import AIMessages, AIMessage

# tiktoken is a fast BPE tokeniser for use with OpenAI's models.

# TODO:
# pydantic is a dynamic data validator 
# type of data to be received or sent to openai endpoint.
# should also be implemented in udpComms! 
# i think it is already implemented with json.loads/dumps, 
# so load and then dump again to validate, or vice versa.
from pydantic import BaseModel

from openai.types import ChatModel
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam
from openai.types import CreateEmbeddingResponse, Embedding
from openai.types import Model, ModelDeleted

from typing import List, Optional
from utils import API_KEY

# class OpenAI(SyncAPIClient):
#     completions: resources.Completions
#     chat: resources.Chat
#     embeddings: resources.Embeddings
#     files: resources.Files
#     images: resources.Images
#     audio: resources.Audio
#     moderations: resources.Moderations
#     models: resources.Models
#     fine_tuning: resources.FineTuning
#     beta: resources.Beta
#     batches: resources.Batches
#     uploads: resources.Uploads
#     with_raw_response: OpenAIWithRawResponse
#     with_streaming_response: OpenAIWithStreamedResponse

#     # client options
#     api_key: str
#     organization: str | None
#     project: str | None


# OUR USE CASE:

#     completions: resources.Completions
#     chat: resources.Chat
#     embeddings: resources.Embeddings
#     models: resources.Models
#     api_key: str

class OpenAIComms():
    """class responsible for sending messages to openAI API """

    def __init__(self):
        self.client = None    
        self.model_name = None

    def init(self, model:str, max_length=50, max_retry_attempts=3, retry_wait_time=60):
        """
        if model name is not valid, it raises a value exception error. 

        Args:
            model (str): _description_
            max_length (int): _description_
            max_retry (int, optional): _description_. Defaults to 3.
            wait_time (int, optional): _description_. Defaults to 60.

        Raises:
            ValueError: _description_
        """
        if not self._check_valid_model_chat(model):
            raise ValueError("The model type does not exist or is not camptabible for chat completion.")

        self.model_name = model
        self.client = OpenAI(
                            api_key=API_KEY,
                            max_retries=max_retry_attempts, 
                            timeout=retry_wait_time)
        self.max_tokens = max_length
       
    def send_chat(self, prompt:AIMessages) -> (str | None):
        """send a prompt to openAI endpoint for chat completions.

        Args:
            prompt (AIMessages): _description_

        Returns:
            _type_: _description_
        """
        if len(prompt) == 0:
            return None
        return self._request(prompt)

    def send_embedding(self, keywords:str) ->  (Embedding | None):
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

    # ---------
    #  PRIVATE
    # ---------
    
    def _request(self, messages: AIMessages) -> Optional[str] | None :
        """
        roles of the messages should be "system", "user", "assistant". 

        Args:
            messages (AIMessages): the messages for chat completion. 

        Returns:
            Optional[str]: the completion of the provided chat. 
        """
        # ChatCompletionMessageParam
        # ChatCompletionUserMessageParam
        # ChatCompletionAssistantMessageParam
    
        try :
            response = self.client.chat.completions.create(
                model= self.model_name,
                messages= messages.get_messages_formatted(),
                
                max_tokens= self.max_tokens
            )
        except Exception as e : 
            print("openAI request failed")
            print(e)
            return None

        # see openai.yaml under 
        # CreateChatCompletionResponse schema  
        # ChatCompletionResponseMessage schema
        # also see python_client.md

        # choose first message option if there are multiple options.
        return response.choices[0].message.content
    
    def _requese_emb(self, keywords: str, model_name="text-embedding-3-small") -> List[Embedding] | None:
        try :
            response:CreateEmbeddingResponse = self.client.embeddings.create(
                model= model_name,
                input= keywords
            )
        except Exception as e : 
            print("openAI request failed")
            print(e)
            return None

        return response.data

    def _check_valid_model_chat(self,model:str):
        """
            check if the model type does exist. 
            And if it exists, check if it compatible for chat completion.
        Args:
            model (str): model id
        """

        return model in str(ChatModel)
    
    def _check_valid_model_emb(self,model:str):
        """
            check if the model type does exist. 
            And if it exists, check if it compatible for chat completion.
        Args:
            model (str): model id
        """

        return model in ["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"]

if __name__ == "__main__":
    x = OpenAIComms()
    x.init("gpt-4")

    aimessages = AIMessages()
    aimessages.add_message(AIMessage("Hi", "assistant"))

    res = x.send_chat(aimessages)
    res2 = x.send_embedding("gagagagagagagagga")
    if res :
        print("LETS GOO")
    else :
        print("DAS IST EINE KOLOSALE KONSPIRAZION  ~Luis de Funes")