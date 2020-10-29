from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from CreateDB import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# myFirstRestaurant = Restaurant(name="Sachdeva")
# session.add(myFirstRestaurant)
# session.commit()
myRestaurant = session.query(Restaurant).filter_by(id=1).one()
cheezepizza = MenuItem(name="Tangy Onion", id = 8, price="$ 2.50",  restaurant = myRestaurant)
session.add(cheezepizza)
session.commit()
# restaurants = session.query(Restaurant).all()
# for restaurant in restaurants:
#     print(restaurant.name)
