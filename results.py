class Results: 
    def __init__(self, data, country):
        data = None if not data else data[0]
        self.country = country 
        self.date = "null" if not data else data[0][0]
        self.attendees = [] if not data else data[1]
        
    def json_results(self):
        return {
            "attendeeCount":len(self.attendees),
            "attendees":self.attendees,
            "name":self.country,
            "startDate":self.date
        }