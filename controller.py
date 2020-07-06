from datetime import datetime, timedelta
import holidays


class Controller(object):
    def __init__(self):
        self._start_hour = 8
        self._stop_hour = 17
        self._one_day_secs = 32400

        self._sa_holidays = holidays.SouthAfrica()

    def datetime_valid(self, dt_str):
        try:
            datetime.fromisoformat(dt_str)
        except:
            return False
        return True

    def include_date(self, date_check):
        weekno = date_check.weekday()

        if weekno < 5 and not self._sa_holidays.get(date_check):
           return True
        else:
           return False

    def working_days(self, time_data):
        # Calculating how many full work days there are excluding the dates itself.
        delta = timedelta(days=1)
        start = time_data['start_time'] + delta
        full_work_days = (time_data['end_time'] - time_data['start_time']).days - 1
        if full_work_days < 0:
            full_work_days = 0

        exclude_days = 0
        while start <= time_data['end_time']:
            if not self.include_date(start):
                exclude_days += 1
            start += delta

        return (full_work_days - exclude_days) * self._one_day_secs

    def seconds_between(self, time_data):
        for key in time_data:  # Formatting time
            time_data[key] = datetime.fromisoformat(time_data[key]).replace(tzinfo=None)

        if time_data['start_time'].hour < self._start_hour:  # If start time is before the start time. We move the time.
            time_data['start_time'] = time_data['start_time'].replace(hour=self._start_hour,
                                                                      minute=0,
                                                                      second=0,
                                                                      microsecond=0
                                                                      )

        if time_data['end_time'].hour >= self._stop_hour:  # If end time is after the stop time. We move the time.
            time_data['end_time'] = time_data['end_time'].replace(hour=self._stop_hour,
                                                                  minute=0,
                                                                  second=0,
                                                                  microsecond=0
                                                                  )

        first_day_secs = 0
        if self.include_date(time_data['start_time']):
            first_day_end = datetime.strptime('%s%s%s%s0000' % (time_data['start_time'].year,
                                                      time_data['start_time'].month,
                                                      time_data['start_time'].day,
                                                      self._stop_hour
                                                      ), '%Y%m%d%H%M%S')
            first_day_secs = (first_day_end - time_data['start_time']).seconds

        last_day_secs = 0
        if self.include_date(time_data['end_time']):
            last_day_start = datetime.strptime('%s%s%s%s0000' % (time_data['end_time'].year,
                                                      time_data['end_time'].month,
                                                      time_data['end_time'].day,
                                                      self._start_hour
                                                      ), '%Y%m%d%H%M%S')
            last_day_secs = (time_data['end_time'] - last_day_start).seconds

        include_days = self.working_days(time_data)
        return str(include_days + first_day_secs + last_day_secs)

    def process(self, time_data):
        if not self.datetime_valid(time_data['start_time']) or not self.datetime_valid(time_data['end_time']):
            return 'Invalid time data/format'

        business_seconds = self.seconds_between(time_data)
        return business_seconds
