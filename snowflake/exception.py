from rest_framework.exceptions import APIException

class MissingProductIdException(APIException):
    status_code = 400
    default_detail = 'product id는 필수입니다.'