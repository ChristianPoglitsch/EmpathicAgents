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