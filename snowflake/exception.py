from rest_framework.exceptions import APIException

class MissingProductIdException(APIException):
    status_code = 400
    default_detail = 'product id는 필수입니다.'

class JWTDecodeError(APIException):
    status_code = 400
    default_detail = '올바르지 않은 토큰입니다. 다시 시도해주세요.'

class InvalidEmailError(APIException):
    status_code = 400
    default_detail = '이메일 정보를 읽어오는데 실패했습니다. 다시 시도해주세요.'
