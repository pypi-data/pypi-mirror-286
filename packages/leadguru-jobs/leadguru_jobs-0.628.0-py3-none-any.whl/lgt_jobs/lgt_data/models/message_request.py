from lgt_jobs.lgt_data.enums import SourceType
from lgt_jobs.lgt_data.model import ChatMessage, DedicatedBotModel


class MessageRequest(ChatMessage):
    hidden: bool = False
    source_type: SourceType

    @classmethod
    def from_slack_response(cls, bot: DedicatedBotModel, message_data: dict, sender_id: str):
        message = super().from_slack_response(bot, message_data, sender_id)
        message_request = MessageRequest.from_dic(message.to_dic())
        message_request.source_type = bot.source.source_type
        return message_request
