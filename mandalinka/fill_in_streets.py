#first run get_cities_csv form bash, and download ULICE.csv from slovak post website if not already downloaded
#run python3 manage.py shell and copy paste the following code

from home.models import CityDistrictPostal, Streets


with open('city_street_postal_dpost_distr.csv', 'r') as file:
    next(file)
    for line in file:
        city, street, postal, dpost, district = map(lambda x: x.strip(), line.split(';'))
        obj = CityDistrictPostal.objects.create(city=city, street=street, postal=postal, district=district, country="SK")
        obj.save()

with open('ULICE.csv', 'r') as file:
    next(file)
    for line in file:
        street = line.split(',')[0].replace('. ', '.').strip()
        already = [x.street for x in Streets.objects.filter(street=street)]
        if street not in already:
            obj = Streets.objects.create(street=street)
            obj.save()
