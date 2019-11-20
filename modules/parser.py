from .calconv import Calendar # It will import, trust me

class Parser():
    '''
    The parser module for the main program
    '''
    def __init__(self):
        self.dotw_name ={1: 'Thứ Hai',
                         2: 'Thứ Ba',
                         3: 'Thứ Tư',
                         4: 'Thứ Năm',
                         5: 'Thứ Sáu',
                         6: 'Thứ Bảy',
                         7: 'Chủ Nhật'}

    def parse(self, timetable, iso_date, data_type):
        '''
        Parse the data into a format that `tabulate.tabulate()` can use
        
        Input data type:
        `timetable`: `dict` of a timetable straight from server.
        `iso_date` `tuple` or `list` of length 3
        `data_type`: Either `'daily'` or `'weekly'` This will affect the final output
        '''
        # Initial sanity check
        if data_type not in ['daily', 'weekly']:
            raise ValueError('data_type must be either "daily" or "weekly"')
        
        # Extracting all necessary date-time data 
        year, week, day = iso_date

        # Preliminary filtering for entries that falls into the given week
        week_match = [i for i in timetable if (str(week) in i['tuan_hoc'].split('|'))]

        # Initial formatting for everything
        result = [[f'{self.dotw_name[entry["thu1"] - 1]}\n'# Date of the week
                   f'{Calendar().iso_to_gregorian((year, week, entry["thu1"] - 1))}', # The day
                   f'{entry["giobd"]} - {entry["giokt"]}',  # Time of class
                   f'{entry["phong1"]}',                    # Room number
                   f'{entry["ten_mh"].strip()}']            # Subject name
                   for entry in week_match] or 'Không có dữ liệu'
        
        # Filter down if requested for daily data
        if data_type == 'daily':
            result = ([entry[1:] for entry in result if (self.dotw_name[day] in entry[0])] 
                       or 'Không có dữ liệu')
        return result
