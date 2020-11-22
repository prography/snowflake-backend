from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Like
from labs.models import Sutra, SutraComment


@receiver(post_save, sender=Like)
def like_post_save(sender, **kwargs):
    like = kwargs['instance']
    model_name = like.content_type.model
    object_id = like.object_id
    if model_name == 'sutra':
        models = Sutra.objects.get(id=object_id)
        models.likes_count += 1
        models.save()
    elif model_name == 'sutracomment':
        models = SutraComment.objects.get(id=object_id)
        models.likes_count += 1
        models.save()


@receiver(post_delete, sender=Like)
def like_post_delete(sender, **kwargs):
    like = kwargs['instance']
    model_name = like.content_type.model
    object_id = like.object_id
    if model_name == 'sutra':
        models = Sutra.objects.get(id=object_id)
        models.likes_count -= 1
        models.save()
    elif model_name == 'sutracomment':
        models = SutraComment.objects.get(id=object_id)
        models.likes_count -= 1
        models.save()
