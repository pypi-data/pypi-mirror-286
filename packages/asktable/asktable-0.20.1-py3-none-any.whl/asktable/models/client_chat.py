from atcommon.models import ChatCore
from atcommon.tools import format_time_ago
from asktable.models.client_base import convert_to_object, BaseResourceList
from asktable.models.client_run import RunList
from asktable.models.client_bot import BotList
from asktable.models.client_msg import MessageList, MessageClientModel
from asktable.api import APIRequest
from atcommon.tools import gen_id


class ChatClientModel(ChatCore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(endpoint=f"{self.endpoint}/{self.id}", method="DELETE")

    @property
    def runs(self):
        return RunList(self.api, endpoint=f"{self.endpoint}/{self.id}/runs")

    @property
    def messages(self):
        return MessageList(self.api, endpoint=f"{self.endpoint}/{self.id}/messages")

    @convert_to_object(cls=MessageClientModel)
    def ask(self, question) -> MessageClientModel:
        # 提问
        data = {"question": question}
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}", method="POST", data=data
        )


class ChatList(BaseResourceList):
    __do_not_print_properties__ = ["tenant_id"]

    @convert_to_object(cls=ChatClientModel)
    def _get_all_resources(self):
        return self._get_all_chats()

    def _get_all_chats(self):
        chats = self._get_all_resources_request()
        # 转换 created 字段
        for chat in chats:
            chat["created"] = format_time_ago(chat["created"])
            chat["latest_msg"] = format_time_ago(chat["latest_msg"])
        return chats

    @property
    @convert_to_object(cls=ChatClientModel)
    def latest(self):
        return self._get_latest_one_or_none()

    def page(self, page_number=1):
        return ChatList(self.api, self.endpoint, page_number=page_number)

    def all(self):
        return ChatList(self.api, self.endpoint, page_number=0, page_size=0)

    @convert_to_object(cls=ChatClientModel)
    def get(self, id):
        # 通过资源ID来获取
        return self.api.send(endpoint=f"{self.endpoint}/{id}", method="GET")

    @convert_to_object(cls=ChatClientModel)
    def create(self, datasource_ids: list = None, bot_id: str = None, **kwargs):

        if bot_id:
            pass
        elif datasource_ids:
            # check datasource_ids
            if any(not isinstance(ds_id, str) for ds_id in datasource_ids):
                raise ValueError(
                    f"datasource_ids must be a list of str: {datasource_ids}"
                )

            bot_admin = BotList(self.api, endpoint="/bots")
            bot_name = f"自动创建-{gen_id()[:10]}"
            bot = bot_admin.create(
                name=bot_name, datasource_ids=",".join(datasource_ids)
            )
            bot_id = bot.id
        else:
            raise ValueError("bot_id or datasource_ids must be provided")

        data = {"bot_id": bot_id, **kwargs}
        return self.api.send(endpoint=self.endpoint, method="POST", data=data)
