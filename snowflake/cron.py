from reviews.models import ReviewCondom
from products.models import Condom
from django.db.models import F


def update_condom_score():
    # condom 점수, 리뷰 개수 초기화
    for condom in Condom.objects.all():
        print(condom)
        condom.score = 0
        condom.avg_oily = 0
        condom.avg_durability = 0
        condom.avg_thickness = 0
        condom.num_of_reviews = 0
        condom.save()

    # condom 점수, 래뷰 개수 업데이트
    for review in ReviewCondom.objects.all():
        total = review.total
        oily = review.oily
        thickness = review.thickness
        durability = review.durability
        product = review.product
        condom = Condom.objects.filter(pk=product).update(
            score=F("score") + total,
            avg_oily=F("avg_oily") + oily,
            avg_thickness=F("avg_thickness") + thickness,
            avg_durability=F("avg_durability") + durability,
            num_of_reviews=F("num_of_reviews") + 1,
        )
