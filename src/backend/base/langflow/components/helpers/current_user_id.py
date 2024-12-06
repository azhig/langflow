from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema.message import Message
# from langflow.services.auth.utils import get_current_active_user


class MemoryComponent(Component):
    display_name = "Current user_id"
    description = "Return current user id or fake"
    icon = "message-square-more"
    name = "current_user_id"

    inputs = [
        MessageTextInput(
            name="fake_current_user_id",
            display_name="Fake Current User ",
            info="Fake current user replace"
        )
    ]

    outputs = [
        Output(display_name="User ID", name="user_id", method="current_or_fake_user_id"),
    ]

    def current_or_fake_user_id(self) -> Message:
        user_id = self.fake_current_user_id or str(self.user_id)
        self.status = self.user_id
        return Message(text=user_id)