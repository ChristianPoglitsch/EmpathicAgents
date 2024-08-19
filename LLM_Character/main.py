import torch
import time

from LLM_Character.llm_api import LLM_API
from LLM_Character.udp_comms import UdpComms
from LLM_Character.messages_dataclass import AIMessages 
from LLM_Character.world.message_processor import MessageProcessor
from LLM_Character.world.game import ReverieServer

# TODO: 
# there must be a way to add location to spatial memory, because now it is hardcoded which is less ideal. 
    
def start_server(sock:UdpComms,
                 server:ReverieServer,
                 dispatcher:MessageProcessor, 
                 model:LLM_API):

    while True:
        time.sleep(1)
        byte_data = sock.ReadReceivedData()
        if not byte_data:
            continue  

        value = dispatcher.validate_data(str(byte_data))
        if value is None:
            continue
        
        dispatcher.dispatch(sock, server, model, value)


if __name__ == "__main__":
    from LLM_Character.llm_comms.llm_local import LocalComms
    from LLM_Character.llm_comms.llm_openai import OpenAIComms 

    # Set HF_HOME for cache folder
    # CUDA recommended!
    print("CUDA found " + str(torch.cuda.is_available()))

    # model_id = "meta-llama/Meta-Llama-3-8B"
    # model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1" 
    # model_id = "google/gemma-7b"
    # model_id = "mistralai/Mistral-7B-Instruct-v0.2"
    model_id = "cerebras/Cerebras-GPT-256M"

    modelc = LocalComms()
    # modela = OpenAIComms()
    modelc.init(model_id)
    model = LLM_API(modelc)

    sock = UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)
    dispatcher = MessageProcessor()

    # place where all variables are initialised if not provided by unity server. (TODO) 
    fork_sim_code= "initial"
    sim_code ="new"

    server = ReverieServer(fork_sim_code, sim_code)
    start_server(sock, server, dispatcher, model)
