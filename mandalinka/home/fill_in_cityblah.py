from models import CityDistrictPostal

#first run 'bash get_cities_csv.sh [filename(optional)]' to create a csv file and then change the open filename in the following script

with open("city_street_postal_dpost_distr.csv", "r") as f:
    f.readlines(1)
    for line in f:
        city, street, postal, dpost, district = map(lambda x: x.strip(), line.split(';'))
        object = CityDistrictPostal.objects.create(city=city, street=street, postal=postal, district=district, country="SK")
        object.save()