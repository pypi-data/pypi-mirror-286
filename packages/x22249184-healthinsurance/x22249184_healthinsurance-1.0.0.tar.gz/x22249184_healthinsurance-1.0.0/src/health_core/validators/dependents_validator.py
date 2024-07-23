from ..exceptions.health_exception import DependentException, ClaimException

def validate_depenent(relation, age):
    if relation == 'Child' and age >= 18:
        raise DependentException('age: Child age must be less than 18.')

def check_dependent(dependent, objects):
    validate_depenent(dependent.relation, dependent.age)
    if objects.filter(name=dependent.name, user = dependent.user).count() > 0:
        raise DependentException("name:  a dependent with name already exists")