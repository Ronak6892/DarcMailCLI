#############################################################
# 2016-09-28: MessageProcessor.py
# Author: Jeremy M. Gibson (State Archives of North Carolina)
#
# Description:
##############################################################
from email.message import Message
from eaxs.MultiBodyType import MultiBody
from eaxs.SingleBodyType import SingleBody
import logging


class MessageProcessor:
    """"""

    def __init__(self, message, relpath):
        """Constructor for MessageProcessor
        :type message : Message
        """
        self.message = message  # type: Message
        self.multipart = message.is_multipart()
        self.payloads = message.get_payload()  # type: list[Message]
        self.single_bodies = []  # type: list[SingleBody]
        self.relpath = relpath
        self.logger = logging.getLogger()

    def process_payloads(self):
        multi_body = MultiBody(self.message)
        multi_body.process_headers()
        for payload in self.payloads:
            '''
            :type payload : Message
            '''
            try:
                if payload.is_multipart():
                    # TODO: Handle this.
                    pass
                else:
                    single_body = SingleBody(payload)
                    single_body.process_headers()
                    single_body.process_body()
                    single_body.payload = None
                    self.single_bodies.append(single_body)
            except AttributeError as e:
                self.logger.error("{}".format(e))
        multi_body.single_bodies = self.single_bodies
        multi_body.payload = None
        return multi_body
