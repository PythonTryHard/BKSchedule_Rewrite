from datetime import datetime, date, time, timedelta

class Calendar():
    '''
    Ah yes, everyone's favorite headache: Calendar and time format.
    '''
    def _iso_year_start(self, iso_year):
        '''
        The gregorian calendar date of the first day of the given ISO year
        '''
        fourth_jan = date(iso_year, 1, 4)
        delta = timedelta(fourth_jan.isoweekday() - 1)
        return fourth_jan - delta
    
    def iso_to_gregorian(self, iso_date):
        '''
        Gregorian calendar date for the given ISO year, week and day

        Input data type:
        - `iso_date`: `tuple` of length(3), formatted to (year, month, day)

        Output:
        `datetime` object       
        '''
        # Unpack the given tuple
        iso_year, iso_week, iso_day = iso_date
        
        # Calculate the the day of ISO year given
        year_start = self._iso_year_start(iso_year)
        gregorian_date = year_start + timedelta(days=iso_day - 1, weeks=iso_week - 1)
        
        return gregorian_date