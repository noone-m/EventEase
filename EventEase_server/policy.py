"""
the finantial policy of the app is written here 
"""


import typing
from datetime import datetime, timedelta
from accounts.models import User
from services.models import ServiceReservation



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
    if 0 <= time_passed_to_the_whole_time <= 10:
        return 0
    elif 10 < time_passed_to_the_whole_time <= 20:
        return 0.04
    elif 10 < time_passed_to_the_whole_time <= 20:
        return 0.08
    elif 10 < time_passed_to_the_whole_time <= 20:
        return 0.12
    elif 10 < time_passed_to_the_whole_time <= 20:
        return 0.16
    elif 10 < time_passed_to_the_whole_time <= 20:
        return 0.2
    elif 10 < time_passed_to_the_whole_time <= 20:
        return 0.24
    elif 10 < time_passed_to_the_whole_time <= 20:
        return 0.28
    elif 10 < time_passed_to_the_whole_time <= 20:
        return 0.32
    elif 10 < time_passed_to_the_whole_time <= 20:
        return 0.36
    
def get_refund_after_cancelling_service_reservation(user:User,reservation:ServiceReservation):
    from wallet.models import CenterWallet
    """
    return how much refund should be if user or service provider has cancelled a service reservation
    Args:
        user (User): the user who made the cancellation
        reservation (ServiceReservation): the service reservation

    Returns:
        value(number) : the value of refund
    """
    reservation_start_time = reservation.start_time
    reservation_made_at = reservation.created_at
    cancellation_time = datetime.now()
    time_passed = reservation_made_at - cancellation_time # the time that has passed when the reservation was made
    time_to_reservation = reservation_start_time - cancellation_time # how much time there is to reach the reservation
    whole_time_span = reservation.created_at - reservation.start_time # the whole time span between when the reservation is made and when it will took place
    if user == reservation.service.service_provider:
        center_wallet = CenterWallet.objects.first()
        center_wallet.refund()
        if time_to_reservation <= timedelta(hours=24):
            return reservation.cost + reservation.cost * 0.5
        return reservation.cost + reservation.cost * get_compensation_percentage(time_passed,whole_time_span)
    elif user == reservation.event.user: # we multiply by 0.5 because that is how much money service provider pay when the reservation is made
        if time_to_reservation <= timedelta(hours=24):
            return RESERVATION_PROTECTION_PERCENTAGE* reservation.cost + reservation.cost * 0.5
        return RESERVATION_PROTECTION_PERCENTAGE * reservation.cost + reservation.cost * get_compensation_percentage(time_passed,whole_time_span)