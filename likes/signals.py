from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import Like
from labs.models import Sutra, SutraComment
from products.models import Product
from reviews.models import Review


model_dict = {
    'sutra': Sutra,
    'product': Product,
    'review': Review,
    'sutracomment': SutraComment
}


@receiver(post_save, sender=Like)
def like_post_save(sender, **kwargs):
    like = kwargs['instance']
    model_name = like.content_type.model
    object_id = like.object_id

    obj = model_dict[model_name].objects.get(id=object_id)
    obj.likes_count += 1
    obj.save()


@receiver(post_delete, sender=Like)
def like_post_delete(sender, **kwargs):
    like = kwargs['instance']
    model_name = like.content_type.model
    object_id = like.object_id
    # obj이 삭제되어 연쇄적으로 like가 삭제되는 경우에는 obj이 존재하지 않는다.
    try:
        obj = model_dict[model_name].objects.get(id=object_id)
    except ObjectDoesNotExist:
        return
    obj.likes_count -= 1
    obj.save()
