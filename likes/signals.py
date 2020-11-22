from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Like
from labs.models import Sutra
from products.modesl import Product


@receiver(post_save, sender=Like)
def like_post_save(sender, **kwargs):
    like = kwargs['instance']
    model_name = like.content_type.model
    object_id = like.object_id
    if like.content_type.model == 'sutra':
        sutra = Sutra.objects.get(id=object_id)
        sutra.likes_count += 1
        sutra.save()
    elif like_content_type.model == 'product':
        obj = Product.objects.get(id=object_id)
        obj.num_of_likes += 1
        obj.save()
	elif like_content_type.model == 'review':
		obj = Product.objects.get(id=object_id)
        obj.num_of_likes += 1
        obj.save()


@receiver(post_delete, sender=Like)
def like_post_delete(sender, **kwargs):
    like = kwargs['instance']
    model_name = like.content_type.model
    object_id = like.object_id
    if like.content_type.model == 'sutra':
        sutra = Sutra.objects.get(id=object_id)
        sutra.likes_count -= 1
        sutra.save()
	elif like_content_type.model == 'product':
        obj = Product.objects.get(id=object_id)
        obj.num_of_likes -= 1
        obj.save()
	elif like_content_type.model == 'review':
		obj = Product.objects.get(id=object_id)
        obj.num_of_likes -= 1
        obj.save()
