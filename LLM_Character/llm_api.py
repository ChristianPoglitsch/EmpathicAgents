""" summary """ 

from dataclass import AIMessages, AIMessage

from llm_comms.llm_abstract import LLMComms
from llm_comms.llm_local import LocalComms
from llm_comms.llm_openai import OpenAIComms

# in order to prevent the terminal to be cluttered from all the torch/transformers warnings. 
import warnings
import logging

warnings.filterwarnings('ignore')
logging.getLogger('transformers').setLevel(logging.ERROR)

# make safe request by making the prompt safe. see gpt_structure. 

#   prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
#   prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
#   prompt += "Example output json:\n"
#   prompt += '{"output": "' + str(example_output) + '"}'

class LLM_API():
    """
    A class to handle operations related to LLM models, 
    including loading models, querying models, and summarizing messages.
    """
    def __init__(self, LLMComms:LLMComms):
        self._model = LLMComms

    def query(self, prompt: AIMessage, message:AIMessages) -> tuple[AIMessages, str]:
        """
        Query the model with a given chat.
        
        Returns:
            tuple: A tuple containing the updated messages and the model's response.
        """

        messages.add_message(messages.create_message(prompt.get_message(), "user"))
        response = self._model.send_text(message)
        message = AIMessage(response, "assistant")
        messages.add_message(message)
        return messages, response
    
    # QUESTION: Why only summarise user messages of the chat?
    # FIXME: todo.md
    def query_summary(self, chat:AIMessages) -> tuple[AIMessages, str]:
        user_messages_concatenated = chat.get_user_message()
        message = AIMessage("Summerize the chat: " + user_messages_concatenated.get_user_message(), "user") 
        
        messages = AIMessages()
        messages.add_message(message)

        response = self._model.send_text(summary)
        message = AIMessage(response, "assistant")
        messages.add_message(message)
        return messages, response


    def semantic_relationship(sef, text1:str, text2:str) -> int:
        """ 
        Calculates how close the two given texts are semantically.
        """
        pass


if __name__ == "__main__":
    x = LocalComms()
    model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    x.init(model_id)

    # y = OpenAIComms()
    # model_id = "gpt4"
    # y.init(model_id)
    
    hf = LLM_API(x)
    # hf = LLM_API(y)
    
    messages = AIMessages()
    m1 = AIMessage("Hello, how are you?", "user")
    m2 = AIMessage("I'm fine, thank you! How can I assist you today?", "assistant")
    m3 = AIMessage("Can you tell me a joke?", "user")
    m4 = AIMessage("Why don't scientists trust atoms? Because they make up everything!", "assistant")
    
    messages.add_message(m1)
    messages.add_message(m2)
    messages.add_message(m3)
    messages.add_message(m4)
    
    updated_messages, response = hf.query("what?", messages)
    
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
