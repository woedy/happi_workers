from datetime import datetime, timedelta
from random import choice

import pytz
from rest_framework.response import Response


def set_rucurring_slot(request):
    REPEAT_ON_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly')
    ]

    END_REPEAT_CHOICES = [
        ('Never', 'Never'),
        ('on', 'on'),
        ('After', 'After'),
    ]

    if request.method == 'POST':
        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')
        repeat = request.data.get('repeat')
        repeat_every = int(request.data.get('repeat_every', 1))
        repeat_on = request.data.get('repeat_on', [])
        repeat_on_day = int(request.data.get('repeat_on_day', 1))
        repeat_on_month = request.data.get('repeat_on_month')
        end_repeat = request.data.get('end_repeat')
        end_repeat_on_str = request.data.get('end_repeat_on')
        end_repeat_after = int(request.data.get('end_repeat_after', 1))
        recurring_time_str = request.data.get('recurring_time')  # Time in 'HH:MM' format
        timezone_str = request.data.get('timezone', 'GMT')

        timezone = pytz.timezone(timezone_str)

        # Convert date string to datetime object with timezone information
        start_date = timezone.localize(datetime.strptime(start_date_str, '%Y-%m-%d')).date()
        end_date = timezone.localize(datetime.strptime(end_date_str, '%Y-%m-%d')).date() if end_date_str else None
        end_repeat_on = timezone.localize(datetime.strptime(end_repeat_on_str, '%Y-%m-%d')).date() if end_repeat_on_str else None

        recurring_time = datetime.strptime(recurring_time_str, '%H:%M').time()

        # Validate parameters (you may want to add more validation logic)
        if repeat not in [choice[0] for choice in REPEAT_ON_CHOICES]:
            return Response({'error': 'Invalid repeat option'}, status=400)

        if end_repeat not in [choice[0] for choice in END_REPEAT_CHOICES]:
            return Response({'error': 'Invalid end repeat option'}, status=400)

        recurring_slots = generate_recurring_slots_with_time_and_repeat_on(
            start_date, end_date, repeat, repeat_every,
            repeat_on, repeat_on_month, repeat_on_day,
            end_repeat, end_repeat_on, end_repeat_after,
            recurring_time=recurring_time
        )

        return Response({'recurring_dates': [date.isoformat() for date in recurring_slots]})

    return Response({'error': "Invalid request method"}, status=400)


def generate_recurring_slots_with_time_and_repeat_on(start_date, end_date, repeat, repeat_every,
                                       repeat_on_list, repeat_on_month, repeat_on_day,
                                       end_repeat, end_repeat_on, end_repeat_after,
                                       recurring_time):

    recurring_slots = []

    current_date = start_date
    while current_date <= end_date:
        # Check if the current date satisfies the repeat conditions
        if is_repeating_with_repeat_on(current_date, repeat, repeat_on_list, repeat_on_month, repeat_on_day):
            # Combine the date and user-provided time to create a datetime object
            recurring_datetime = datetime.combine(current_date, recurring_time)
            recurring_slots.append(recurring_datetime)

        # Move to the next date based on the repeat frequency
        current_date += timedelta(days=repeat_every)

        # Check if we've reached the end repeat condition
        if is_end_reached(current_date, end_repeat, end_repeat_on, end_repeat_after):
            break

    return recurring_slots


MONTH_CHOICES = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}


def is_repeating_with_repeat_on(current_date, repeat, repeat_on_list, repeat_on_month, repeat_on_day):
    # Implement logic to check the current date satisfies the repeat conditions

    if repeat == 'Daily':
        return True

    elif repeat == 'Weekly':
        # Check if the current day of the week is in the repeat_on_list
        return str(current_date.weekday()) in repeat_on_list

    elif repeat == 'Monthly':
        # Check if the current day of the month matches the specified repeat_on_day
        return  current_date.day == repeat_on_day

    elif repeat == 'Yearly':
        # Check if the current day, month. and year matches the specified repeat_on_day, repeat_on_month, and current year
        return (
            current_date.day == repeat_on_day and
            current_date.month == MONTH_CHOICES[repeat_on_month] and
            current_date.year == datetime.now().year

        )

    return False


def is_end_reached(current_date, end_repeat, end_repeat_on, end_repeat_after):
    # Implement logic to check if the end repeat conditions are met
    if end_repeat == 'Never':
        return False

    elif end_repeat == 'on':
        return current_date == end_repeat_on

    elif end_repeat == 'After':
        return str(current_date) > str(end_repeat_after)

    return False