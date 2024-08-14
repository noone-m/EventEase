"""
the finantial policy of the app is written here 
"""


import typing
from datetime import datetime, timedelta
from accounts.models import User
from services.models import ServiceReservation
from zoneinfo import ZoneInfo
from django.conf import settings




FEE_PERCENTAGE = 0.05
RESERVATION_PROTECTION_PERCENTAGE = 0.5


def get_compensation_percentage(time_passed:datetime,whole_time_span:datetime):
    """
    return compenstaion percentage
    Args:
        time_passed (datetime): the user who made the cancellation
        whole_time_span (datetime): time difference between the time which reservation is made and reservation start time 

    Returns:
        get_compensation_percentage(number) : the percentage of compensation
    """

    time_passed_to_the_whole_time = time_passed*100/whole_time_span # *100 to get %
    print(time_passed_to_the_whole_time)
    if 0 <= time_passed_to_the_whole_time <= 10:
        return 0
    elif 10 < time_passed_to_the_whole_time <= 20:
        return 0.04
    elif 20 < time_passed_to_the_whole_time <= 30:
        return 0.08
    elif 30 < time_passed_to_the_whole_time <= 40:
        return 0.12
    elif 40 < time_passed_to_the_whole_time <= 50:
        return 0.16
    elif 50 < time_passed_to_the_whole_time <= 60:
        return 0.2
    elif 60 < time_passed_to_the_whole_time <= 70:
        return 0.24
    elif 70 < time_passed_to_the_whole_time <= 80:
        return 0.28
    elif 80 < time_passed_to_the_whole_time <= 90:
        return 0.32
    elif 90 < time_passed_to_the_whole_time <= 100:
        return 0.36
    
def get_refund_after_cancelling_service_reservation(user:User,reservation:ServiceReservation):
    from wallet.models import CenterWallet
    """
    return how much refund should be if user or service provider has cancelled a service reservation
    Args:
        user (User): the user who made the cancellation
        reservation (ServiceReservation): the service reservation

    Returns:
        refund(number) : the value of refund
        compensation(number) : the value of compensation
    """
    reservation_start_time = reservation.start_time
    reservation_made_at = reservation.created_at

    timezone = ZoneInfo(settings.TIME_ZONE)

    # Convert both datetimes to the same timezone
    reservation_made_at = reservation_made_at.astimezone(timezone)
    cancellation_time = datetime.now(timezone)
    time_passed = reservation_made_at - cancellation_time # the time that has passed when the reservation was made
    time_to_reservation = reservation_start_time - cancellation_time # how much time there is to reach the reservation
    whole_time_span = reservation.created_at - reservation.start_time # the whole time span between when the reservation is made and when it will took place
    reservation_cost = float(reservation.cost)
    compensation_percentage = get_compensation_percentage(time_passed,whole_time_span)
    compensation_value = reservation_cost * compensation_percentage
    if user == reservation.service.service_provider:
        # the returns will follow this pattern money paid + fee paid + refund
        if time_to_reservation <= timedelta(hours=24):
            compensation_value = reservation_cost  * RESERVATION_PROTECTION_PERCENTAGE
        return compensation_value, reservation_cost + reservation_cost*FEE_PERCENTAGE  + compensation_value
    elif user == reservation.event.user: 
        if time_to_reservation <= timedelta(hours=24):
            compensation_value = reservation_cost * RESERVATION_PROTECTION_PERCENTAGE
        return compensation_value, RESERVATION_PROTECTION_PERCENTAGE * reservation_cost + RESERVATION_PROTECTION_PERCENTAGE* reservation_cost * FEE_PERCENTAGE + compensation_value