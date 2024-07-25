
class MessageBase:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getitem__(self, item):
        return getattr(self, item)

    def __contains__(self, item):
        return item in self.__dict__

class HumanMessage(MessageBase):
    pass


class AIMessage(MessageBase):
    pass


class SystemMessage(MessageBase):
    pass