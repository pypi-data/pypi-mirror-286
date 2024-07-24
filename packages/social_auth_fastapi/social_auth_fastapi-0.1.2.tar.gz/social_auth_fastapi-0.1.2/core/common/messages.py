from core.common.i18n import i18n as _ 


class Messages:
    def __call__(self, value, language: str = None):
        return  _(value, language)


messages: Messages = Messages()
