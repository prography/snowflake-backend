from django.apps import AppConfig


class LikesConfig(AppConfig):
    name = 'likes'

    def ready(self):
        import likes.signals
