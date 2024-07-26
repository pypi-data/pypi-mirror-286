from lgt_jobs.lgt_data.model import ChatMessage, DedicatedBotModel


class MessageRequest(ChatMessage):
    hidden: bool = False

    @classmethod
    def from_slack_response(cls, bot: DedicatedBotModel, message_data: dict, sender_id: str):
        message = super().from_slack_response(bot, message_data, sender_id)
        return message.from_dic(message.to_dic())
