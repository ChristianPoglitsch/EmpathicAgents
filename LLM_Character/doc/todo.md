* make sure the LlmTraining.py and Main.py work when upgrading `transformers` due to some bug, see bug.md
issue needs to be fixed.

* make sure the destination of writing the chat is redirected to the dialogues folder. (change also needed for data folder)


* See QUESTION in huggingface.py (why only summarize from user messages?) 

>[user] Summerize the chat: Hello, how are you?Can you tell me a joke?   
>[assistant]  In this interaction, the AI greets the user with a standard salutation, "Hello, how are you?" The user then makes a request for a joke to be shared. However, the AI does not provide a joke in response. Instead, the conversation ends with the initial greeting. Thus, the chat summary would be: The user asked for a joke, but the AI did not provide one.  


