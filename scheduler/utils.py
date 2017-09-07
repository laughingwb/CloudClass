
from datetime import timedelta, datetime, date
import dateutil.parser
from django.utils import timezone


def get_monday_of_the_week(t_datetime):
    week_day = t_datetime.weekday()
    # if week_day == 6:
    #    week_day = -1
    monday = t_datetime - timedelta(days=week_day)

    # print('monday is %s' % monday)

    return monday


def get_next_monday_of_the_week(t_datetime):
    week_day = t_datetime.weekday()
    # if week_day == 6:
    #    week_day = -1
    sunday = t_datetime - timedelta(days=week_day) + timedelta(days=7)

    # print('sunday is %s' % sunday)

    return sunday


def get_last_sunday(t_datetime):
    week_day = t_datetime.weekday()
    if week_day == 6:
        week_day = -1
    sunday = t_datetime - timedelta(days=week_day)

    return sunday


def get_localized_datetime(date):
    users_tz = timezone.get_current_timezone()
    print('timezone is {}'.format(users_tz))
    if not date:
        return None

    if type(date) is str:
        if len(date) == 10:
            try:
                t_date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return None
        else:
            t_date = dateutil.parser.parse(date)
    else:
        t_date = date

    if t_date.tzinfo is None or t_date.tzinfo.utcoffset(t_date) is None:
        return users_tz.localize(t_date, is_dst=None)
    else:
        return t_date.astimezone(users_tz)


def get_one_week_range(cur_date, t_default=None, action=None):
    d = cur_date
    if not d:
        if not t_default:
            d_default = date.today()
        else:
            d_default = t_default.date()
        d = d_default.strftime('%Y-%m-%d');

    users_tz = timezone.get_current_timezone()

    t_datetime = get_localized_datetime(d)

    # logger.debug('current_date is: %s, and parsed as %s' % (d, t_datetime))

    if action:
        if action == 'previous':
            t_datetime = t_datetime - timedelta(days=7)
        elif action == 'next':
            t_datetime = t_datetime + timedelta(days=7)

    d = t_datetime.strftime('%Y-%m-%d')

    t_monday = get_monday_of_the_week(t_datetime)
    t_next_monday = get_next_monday_of_the_week(t_datetime)

    return d, t_monday, t_next_monday

def get_hours_in_the_week(t_time):
    return t_time.weekday() * 24 + t_time.hour + t_time.minute/60