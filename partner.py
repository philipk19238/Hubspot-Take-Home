import datetime
class Partner: 
    def __init__(self, data):
        self.email = data['email'] 
        self.country = data['country']
        self.available = data['availableDates']
        
    def convert_date(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')
        
    def get_consecutive(self):
        available_list = []
        for i in range(0, len(self.available) - 1):
            curr_date = self.available[i]
            next_date = self.available[i + 1]
            difference = self.convert_date(next_date) - self.convert_date(curr_date)
            if difference.days == 1: 
                available_list.append(tuple([curr_date, next_date]))
        return available_list