from CreateDB import Base, Restaurant, MenuItem
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///restaurantmenu.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = render_template('menu.html', restaurant=restaurant, items=items)
    return output


@app.route('/restaurants/<int:restaurant_id>/new', methods={'GET', 'POST'})
def addNewItem(restaurant_id):
    if(request.method=="POST"):
        newItem = MenuItem(name=request.form['name'], price = "$ "+request.form['price'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
    else:
        return render_template('NewItem.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods={'GET', 'POST'})
def EditItem(restaurant_id, menu_id):
    if(request.method == "POST"):
        oldItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(id=menu_id).one()
        oldItem.price = "$ "+request.form['price']
        oldItem.name = request.form['name']
        session.add(oldItem)
        session.commit()
        return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
    else:
        return render_template('EditItem.html', restaurant_id=restaurant_id, menu_id=menu_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods={'GET', 'POST'})
def DeleteItem(restaurant_id, menu_id):
    return ("Page to delete")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
