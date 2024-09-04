# General information

## How to start the python endpoint

**1. Navigate to the Project Directory**

Open your terminal or command prompt and change to the EMPATHICAGENTS directory:
```bash
    cd /path/to/EMPATHICAGENTS
```
Replace /path/to/EMPATHICAGENTS with the actual path to your project directory.

**2. Execute the Setup File**

Execute the setup script to install dependencies and set up your environment:

- **On macOS and Linux (and Windwos git bash terminal) :**
```bash
      ./setup.sh
```
- **On Windows:**
```sh
      setup.bat
```
**3. Navigate to the LLM_Character Directory**

Change to the LLM_Character directory:
```bash
    cd /path/to/LLM_Character
```
Replace /path/to/LLM_Character with the actual path to the LLM_Character directory.

**4. Start the Python Endpoint**

Run the main.py script to start the Python endpoint:
```bash
    python main.py
```

## Python API
This is the API offered by the python endpoint (server) which the unity endpoint (client) is calling. 

>StartMessage: Initialize a new game from a saved game or start a new game.
>PromptMessage: Send a prompt (chatting) to a persona.
>MoveMessage: Update the location and events related to a persona.
>UpdateMetaMessage: Update metadata, such as the current time within the game.
>UpdatePersonaMessage: Update the details of a persona, such as their name, age, and location.
>UpdateUserMessage: Change user information (name).
>AddPersonaMessage: Add a new persona to the simulation with specified attributes.
>GetPersonasMessage: Retrieve all personas currently in the game.
>GetUsersMessage: Retrieve all users in the game.
>GetPersonaMessage: Retrieve specific details about a single persona.
>GetSavedGamesMessage: Retrieve a list of saved games.
>GetMetaMessage: Retrieve metadata related to the game.
>ErrorResponse: Handle error scenarios.

## Server Setup and Communication:

start_server: This is the function that launches the server to listen for incoming messages and process them accordingly.

Communication: The script sets up UDP communication channels using the UdpComms class to facilitate message exchange between the client and server. It is a subclass of the abstract class CommMedium which acts as the interface. There is a strategy pattern used here, where you can hand over any object that inherits from this CommMedium to the start_server function in order to start listening.   


