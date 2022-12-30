import requests
from django.conf import settings
from celery import shared_task
import logging
from user.models import User


@shared_task
def save_holiday_for_user(id):
    user = User.objects.get(id=id)
    get_country = requests.get(
        f"https://ipgeolocation.abstractapi.com/v1/?api_key={settings.GEO_IP_KEY}"
    )
    get_holiday = requests.get(
        f"https://holidays.abstractapi.com/v1/?api_key={settings.GEO_HOLIDAY_KEY}&country={get_country.json()['country_code']}&year={int(user.joined_at.year)}&month={int(user.joined_at.month)}&day={int(user.joined_at.day)}"
    )
    if get_country.ok and get_holiday.json():
        user.signed_up_holiday = get_holiday.json()[0]["name"]
        user.save()
    else:
        logging.warning(f"{get_country.json()} || {get_holiday.json()}")
