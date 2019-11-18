import tabulate

class Display():
    '''
    A module dedicated to all thing displaying.
    '''
    def __init__(self):
        '''
        Initialize the table's headers
        '''
        self.daily_table_header = ['Giờ học', 'Môn', 'Phòng']
        self.weekly_table_header = ['Thứ'] + self.daily_table_header

    def display_table(self, table, data_type):
        '''
        Print a table of periods for either a day for a week.

        Input data types:
        - `period_data`: `list` of lists. Each entries' length being 3 or 4 depends on the `data_type`
        - `data_type`: Either `"daily"` or `"weekly"`. This will affect the final table produces on console

        Known exceptions:
        - `ValueError`: Raised when `data_type` doesn't conform to requirement.
        '''
        # Initial sanity check for myself
        if data_type not in ('daily', 'weekly'):
            raise ValueError('data_type only accepts "daily" or "weekly"')
        # Checking data type
        if data_type == 'daily':
            header = self.weekly_table_header
        else:
            header = self.daily_table_header
        # Printing
        print(tabulate.tabulate(table, headers=header, tablefmt='grid'))
        return
