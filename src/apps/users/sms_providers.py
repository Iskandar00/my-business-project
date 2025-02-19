import random
import requests

from django.conf import settings
from django.core.cache import cache


class EskizUz:
    TOKEN_KEY = "eskiz_uz_token"
    AUTH_CODE_KEY = "auth_code_{username}"
    FORGOT_PASSWORD_KEY = "forgot_password_token{token}"

    GET_TOKEN_URL = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    SEND_SMS_URL = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    FORGOT_PASSWORD_MESSAGE = "parolingizni tiklash uchun quyidagi havolaga o'ting {link}"
    AUTH_CODE_MESSAGE = "Aksiyamix websaytiga kirish uchun tasdiqlash kodingiz: {code}"

    EMAIL = "settings.ESKIZ_UZ_EMAIL"
    PASSWORD = "settings.ESKIZ_UZ_PASSWORD"

    @classmethod
    def get_token(cls):
        token = cache.get(cls.TOKEN_KEY)
        if not token:
            response = requests.post(
                url=cls.GET_TOKEN_URL, 
                data={
                    'email': cls.EMAIL,
                    'password': cls.PASSWORD
                    }
                )
            token = response.json()['data']['token']
            cache.set(cls.TOKEN_KEY, token, timeout=60 * 60 * 24 * 29)
        return token

    @classmethod
    def send_sms(cls, send_type: str, username: str, nickname='4546', token=None, link=None):
        if send_type == 'FORGOT_PASSWORD':
            message = cls.FORGOT_PASSWORD_MESSAGE.format(link=link)
            cache.set(cls.FORGOT_PASSWORD_KEY.format(token=token), username, timeout=60*10)

        elif send_type == 'AUTH_CODE':
            code = random.randint(1000, 9999)
            message = code #cls.AUTH_CODE_MESSAGE.format(code=code)
            cache.set(cls.AUTH_CODE_KEY.format(username=username), code, 60 * 10)

        elif send_type == 'AUTH_CODE_EMAIL':
            code = random.randint(1000, 9999)
            message = code
            cache.set(cls.AUTH_CODE_KEY.format(username=username), code, 60 * 10)
        
        else:
            raise ValueError("Invalid send type")
        
        return message

        # headers = {
        #     'Authorization': f'Bearer {cls.get_token()}',
        # }
        # data = {
        #     'mobile_phone': phone_number,
        #     'message': message,
        #     'from': nickname,
        # }
        # response = requests.post(
        #     url=cls.SEND_SMS_URL,
        #     headers=headers,
        #     data=data
        # )
        # if response.status_code == 401:
        #     cache.delete(cls.TOKEN_KEY)
        #     headers = {
        #         'Authorization': f'Bearer {cls.get_token()}',
        #     }

        #     requests.post(
        #         url=cls.SEND_SMS_URL,
        #         headers=headers,
        #         data=data
        #     )