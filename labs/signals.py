from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Sutra, Evaluation


def change_sutra_count(evaluation, sutra, NUM):
    if evaluation.user_type == "PURPLE":
        if evaluation.recommend_type == "RECOMMEND":
            sutra.purple_recommends_count += NUM
        elif evaluation.recommend_type == "UNRECOMMEND":
            sutra.purple_unrecommends_count += NUM

    elif evaluation.user_type == "SKY":
        if evaluation.recommend_type == "RECOMMEND":
            sutra.sky_recommends_count += NUM
        elif evaluation.recommend_type == "UNRECOMMEND":
            sutra.sky_unrecommends_count += NUM
    sutra.save()


@receiver(post_save, sender=Evaluation)
def evaluation_post_save(sender, **kwargs):
    evaluation = kwargs['instance']
    sutra = evaluation.sutra
    change_sutra_count(evaluation, sutra, 1)


@receiver(post_delete, sender=Evaluation)
def evaluation_post_delete(sender, **kwargs):
    evaluation = kwargs['instance']
    sutra = evaluation.sutra
    change_sutra_count(evaluation, sutra, -1)
