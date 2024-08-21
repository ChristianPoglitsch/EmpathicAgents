import torch
import time

from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.communication.udp_comms import UdpComms
from LLM_Character.communication.message_processor import MessageProcessor
from LLM_Character.communication.reverieserver_manager import ReverieServerManager

# NOTE: ibrahim: temporary function that will be replaced in the future by the hungarian team ?
# which will use grpc, for multi client - (multi server?) architecture? 
# somehow a manager will be needed to link the differnt clients to the right available servers. 
def start_server(sock:UdpComms,
                 serverM:ReverieServerManager,
                 dispatcher:MessageProcessor, 
                 model:LLM_API):
    print("listening ...")
    while True:
        time.sleep(1)
        byte_data = sock.ReadReceivedData()
        if not byte_data:
            continue  
        
        print(f"Received some juicy data : {byte_data}")

        value = dispatcher.validate_data(str(byte_data))
        if value is None:
            continue
        dispatcher.dispatch(sock, serverM, model, value)

if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms
    from LLM_Character.llm_comms.llm_openai import OpenAIComms 

    # Set HF_HOME for cache folder
    # CUDA recommended!
    # print("CUDA found " + str(torch.cuda.is_available()))

    # model_id = "meta-llama/Meta-Llama-3-8B"
    # model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1" 
    # model_id = "google/gemma-7b"
    # model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    model_id = "gpt-4"
    # modelc = LocalComms()
    modelc = OpenAIComms()
    modelc.init(model_id)
    model = LLM_API(modelc)

    sock = UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)
    dispatcher = MessageProcessor()

    #NOTE: for example, for each new incoming socket, new process that executes start_server, with shared resource server_manager, messageprocessor;  
    server_manager = ReverieServerManager()
    start_server(sock, server_manager, dispatcher, model)


