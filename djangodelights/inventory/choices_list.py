import pint 
import inspect

list_of_choices = []
ureg = pint.UnitRegistry()
attributes = inspect.getmembers(ureg, lambda member: not inspect.isroutine(member))
for attribute in attributes:
    list_of_choices.append(attribute[0])




