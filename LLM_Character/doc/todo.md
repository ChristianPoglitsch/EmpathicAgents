# see paper for overall explanation of the design.
Ibrahim: add link

# tasks

* would recommend converting from udp to tcp, as the communication doesnt happen frequently, and you want your initial data to be sent in without data loss. 

* find a better way to represent userScratch and personaScratch, because now there is duplicated code. 

* there must be a way to add location to spatial memory, because now it is hardcoded which is less ideal. 

* go through the repo and see if which events code i need to re-add. 

* add seperate `end conversation` prompt instead of relying on the generate_one_utt
since the problem is that you dont know the sentence generated and if that generated sentence ends the conversation or not. So use another prompt with some chat history and that generated new line and see if it ended it or not.  

* do not forget the look variable in the scratch class.

* every open() function can rasie an exception, exception handling needs to be upgraded, since it is non existent at this moment. 

# emotional state

6 emotions, store in the persona. attached to persona, 
updated after each conversation.query llm

so each person has a personality based on the 5 factor model. 
query llm based on chat history and (possibly update the personality)

update facial expression of the avatar based on the personality or emotionanal state. 

# fix typing in this codebase, use the following to avoid circular imports

https://stackoverflow.com/questions/66987434/importing-classes-just-for-typing-in-python
or somehow redesign code to remove the cyclic dependency

another solution would be to give Scratch memory instead of Persona object,since majority of operation are about extracting something
from memory or adding things to memory.

# TODO

* make sure the LlmTraining.py and Main.py work when upgrading `transformers` due to some bug, see bug.md
issue needs to be fixed.

* make sure the destination of writing the chat is redirected to the dialogues folder. (change also needed for data folder)

* See QUESTION in huggingface.py (why only summarize from user messages?) 

>[user] Summerize the chat: Hello, how are you?Can you tell me a joke?   
>[assistant]  In this interaction, the AI greets the user with a standard salutation, "Hello, how are you?" The user then makes a request for a joke to be shared. However, the AI does not provide a joke in response. Instead, the conversation ends with the initial greeting. Thus, the chat summary would be: The user asked for a joke, but the AI did not provide one.  


* refactor train_model method. 

* add project file py for author chris

* why does the LLM return the response as well as the structured response? I dont think that this is the intention. 
    possible solutions could be mentioning in the prompt to not do this. or in the system background/information to not do this. 
    otherwise, finetuning the model on a dataset in which such occurance does not happen.
    see finetuning/generate_data.py 

> I'm sorry, I'm still not able to understand that response. Could you please provide some more context or clarify what you meant by "hzefzf"? I'm here to chat and learn more about you!
> {"Message": "I'm sorry, I'm still not able to understand that response. Could you please provide some more context or clarify what you meant by 'hzefzf'? I'm here to chat and learn more about you!", "Trust": "6", "Time": "11 AM", "Location": "Graz",


* run python files in LLM_Character folder in order to avoid relative paths errors.

* look at soulmachines as well. 

* check if pip env has the same dependencies as written in requirements.txt

> as a matter of fact, delete venv, try re-installing, see if everything works. 
> if it does, start pull request. 

* seach the difference between using .env and using windows registry for storing api keys. 

> While you can provide an api_key keyword argument, we recommend using python-dotenv to add OPENAI_API_KEY="My API Key" to your .env file so that your API Key is not stored in source control.
> source : https://github.com/openai/openai-python
> ibr: advantage of .env files is that they are platform agnostic. So they will work on any linux distro/windows/MacOS.

# The plan : 

1) Extract all the gameobjects in a unity scene, and the name of the scene, and even the hierarchy in the scenes if there are (i dont think there are)
2) send that information to python front end. (other endpoint than what is now implemented)
3) construct a similar maze class. 
4) from the this maze class, we will know if the user (camera in unity) is close or not to the character (generative agent), from there the generarive agent can decide wether to interact with the user or not. If it wants, there could be a text bubble in unity indicating that the character wants to talk to the user. (or something similar) 
this will provide the active participation that we want from our generative agents. 
In the future, it could possible that the character interacts with the gameobejects in the scene, since that information is also sent. 
In the future, it could be handy to let the unity character move on its own in order to execute its actions if needed. (such going to the fridge to eat something, but this is out of scope for now.) 


for now, include a json that assumes the received information from unity. (caled : unity_info.json)
