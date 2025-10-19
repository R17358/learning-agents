from pydantic import BaseModel

class Person(BaseModel):
    name: str
    year: int
    
person_info = {'name':'Ritesh', 'year':2025}

person_obj = Person(**person_info)

def insert_data(person: Person):
    print(person.name)
    print(person.year)
    print("inserted")
    
def update_data(person: Person):
    print(person.name)
    print(person.year)
    print("updated")
    
insert_data(person_obj)

update_data(person_obj)

# babhishek.idolize@tatacapital.com