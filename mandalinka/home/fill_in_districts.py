#run in python3 manage.py shell
from home.models import Districts

with open("okresy.txt", "r" ) as source:
    for aLine in source:
        object= Districts.objects.create( district=aLine.strip())
        object.save()