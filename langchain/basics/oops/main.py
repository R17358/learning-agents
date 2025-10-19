class Country:
    def __init__(self, name, area, currency):
        self.name = name
        self.area = area
        self.currency = currency
        
    def get_details(self):
        return self.name, self.area, self.currency
    
    def update_details(self, name, area, currency):
        self.name = name
        self.area = area
        self.currency = currency
        

class State(Country):
    def __init__(self, name, area, currency):
        super().__init__(name, area, currency)
        

india = Country("India", 32, 'rupees')
japan = Country("Japan", 10, "yen")

details = india.get_details()
print(details)