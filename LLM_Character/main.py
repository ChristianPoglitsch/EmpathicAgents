import logging
import time

from LLM_Character.communication.message_processor import MessageProcessor
from LLM_Character.communication.reverieserver_manager import ReverieServerManager
from LLM_Character.communication.udp_comms import UdpComms
from LLM_Character.llm_comms.llm_api import LLM_API
from LLM_Character.util import LOGGER_NAME

# NOTE: ibrahim: temporary function that will be replaced in the future
# by the hungarian team ?
# which will use grpc, for multi client - (multi server?) architecture?
# somehow a manager will be needed to link the differnt clients to the
# right available servers, which is now implemented by the ReverieServerManager

logger = logging.getLogger(LOGGER_NAME)


def start_server(
    sock: UdpComms,
    serverm: ReverieServerManager,
    dispatcher: MessageProcessor,
    model: LLM_API,
):
    logger.info("listening ...")
    while True:
        time.sleep(1)
        byte_data = sock.ReadReceivedData()
        if not byte_data:
            continue

        logger.info(f"Received some juicy data : {byte_data}")
        value = dispatcher.validate_data(sock, str(byte_data))
        if value is None:
            continue

        # NOTE: should be disptached in a seperate thread, but as python has the GIL,
        # true multithreading won't work. pub-sub mechanism will be needed.
        dispatcher.dispatch(sock, serverm, model, value)
