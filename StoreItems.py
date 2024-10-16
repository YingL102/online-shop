from onlineApp import *

products = [
    { "name": "Yonex Arcsaber 11 Pro", "price": "183.99", "image": "arcsaber11pro.png", "description": "A LEGENDARY RACKET WITH A MODERN TWIST", "environmental_impact_rating": "5" },
    { "name": "Yonex Astrox 88D Pro", "price": "206.99", "image": "astrox88dpro.png", "description": "UNLEASH UNMATCHED POWER AND PRECISION", "environmental_impact_rating": "9" },
    { "name": "Yonex Astrox 88S Pro", "price": "206.99", "image": "astrox88spro.png", "description": "EXECUTE DECISIVE FRONT COURT ATTACKS", "environmental_impact_rating": "8" },
    { "name": "Yonex Astrox 100ZZ", "price": "207.99", "image": "astrox100zz.png", "description": "VERSATILITY IN POWER", "environmental_impact_rating": "7" },
    { "name": "Yonex Nanoflare 800 Pro", "price": "185.99", "image": "nanoflare800pro.png", "description": "DOMINATE THE GAME WITH CUTTING DRIVES", "environmental_impact_rating": "3" },
    { "name": "Yonex Nanoflare 1000Z", "price": "191.99", "image": "nanoflare1000z.png", "description": "STRIKE LIGHTNING INTO YOUR OPPONENTS", "environmental_impact_rating": "2" },
]

with app.app_context():
    db.create_all()

    for items in products:
        newItem = Product(name = items["name"], price = items["price"], image = items["image"], description = items["description"], environmental_impact_rating = items['environmental_impact_rating'])
        db.session.add(newItem)

    db.session.commit()