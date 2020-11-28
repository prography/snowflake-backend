from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Like
from labs.models import Sutra, SutraComment
from products.models import Product
from reviews.models import Review


@receiver(post_save, sender=Like)
def like_post_save(sender, **kwargs):
    like = kwargs['instance']
    model_name = like.content_type.model
    object_id = like.object_id
    if model_name == 'sutra':
        Model = Sutra
    elif model_name == 'product':
        Model = Product
    elif model_name == 'review':
        Model = Review
    elif model_name == 'sutracomment':
        Model = SutraComment
    obj = Model.objects.get(id=object_id)
    obj.likes_count += 1
    obj.save()


@receiver(post_delete, sender=Like)
def like_post_delete(sender, **kwargs):
    like = kwargs['instance']
    model_name = like.content_type.model
    object_id = like.object_id
    if model_name == 'sutra':
        Model = Sutra
    elif model_name == 'product':
        Model = Product
    elif model_name == 'review':
        Model = Review
    elif model_name == 'sutracomment':
        Model = SutraComment
    obj = Model.objects.get(id=object_id)
    obj.likes_count -= 1
    obj.save()
