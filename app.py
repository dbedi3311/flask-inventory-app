from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

import csv

from sqlalchemy.sql.expression import null

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b"|\x8c\x89\xfc\x13\xbd-7\t'\x88g"         #used to render cookies

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    status = db.Column(db.String(100))
    stock = db.Column(db.Integer)
    #price of the item is a Decimal with 2 digits after .
    price = db.Column(db.Numeric(10, 2), nullable=True)
    description = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #whether or not you've updated the inventory for an item
    complete = db.Column(db.Boolean)

#rendering the homepage from base.html providing it with the list of items currently in db
@app.route('/')
def index():
    item_list = Item.query.all()
    #print(item_list)
    return render_template('base.html', item_list=item_list)


#adding an item to to the database triggers a POST request -->
#check that the fields provided were correct: Integer for stock and Decimal for price
#if not, then flash the required changes needed and return the homepage without processing the request
#otherwise add new item to the database and return to homepage, which has been properly updated with the provided field
@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    status = request.form.get("status")
    stock = request.form.get("stock")
    price = request.form.get("price")
    description = request.form.get("description")

    error = False
    if(not (stock.isdigit() or stock == "")):
        error = True
        flash("quantity provided is not an integer!")
    if(not (price.replace('.', '', 1).isdigit() or price == "")):
        error = True
        flash("price provided is not a decimal-valued number!")
    
    if(error == True):
        return redirect(url_for("index"))
    else:
        if stock != "":
            stock = int(stock)
        if price != "":
            price = float("{:.2f}".format(float(price)))
        else:
            price = None
        new_item = Item(title=title, status=status, stock=stock, price=price, description=description, complete=False)
    
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("index"))

#used to change the complete/not completed status of an item
#just negates the Boolean complete for the item in the database
#proof-of-concept that we can modify the fields of an item in the database
@app.route("/update/<int:item_id>")
def update(item_id):
    # update an item
    item = Item.query.filter_by(id=item_id).first()
    item.complete = not item.complete
    db.session.commit()
    return redirect(url_for("index"))

#deleting an item from the database using the id of the item to process the query
@app.route("/delete/<int:item_id>")
def delete(item_id):
    # delete an item
    item = Item.query.filter_by(id=item_id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))

#editing the item can be both a get and post request (get to initially fill the form with the previously entered fields,
# and post to actually make the update)
# if error with entered fields, return back to the edit form page until the form is properly filled.
@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit(item_id):
    #edit an item
    item = Item.query.filter_by(id=item_id).first()
    
    if request.method == "GET":
        return render_template("filledform.html", item=item)

    changedTitle = request.form.get("title")
    changedStatus = request.form.get("status")
    changedStock = request.form.get("stock")
    changedPrice = request.form.get("price")
    changedDescription = request.form.get("description")

    error = False
    if(not (changedStock.isdigit() or changedStock == "")):
        error = True
        flash("quantity provided is not an integer!")
    if(not (changedPrice.replace('.', '', 1).isdigit() or changedPrice == "")):
        error = True
        flash("price provided is not a decimal-valued number!")

    if(error == True):
        return render_template("filledform.html", item=item)

    if(changedStock != ""):
        changedStock = int(changedStock)
    if(changedPrice != ""):
        changedPrice = float("{:.2f}".format(float(changedPrice)))      #to properly format price data
    else:
        changedPrice = None                         #when value not provided
    
    item.title = changedTitle
    item.status = changedStatus
    item.stock = changedStock
    item.price = changedPrice
    item.description = changedDescription

    db.session.commit()
    return redirect(url_for("index"))


#to download the items in the database as a csv
#fetch all the items in the database and simply write them to a csv 
#use send_file method to process download.
@app.route("/download")
def download():
    item_list = Item.query.all()

    productInfo = ['ID', 'Item Title', 'Quantity', 'Order Status', 'Price - $USD', 'Date Created', 'Description']

    #csv output will be a string, so we can nicely format our prices with a $ in front without any harm to the underlying csv data
    with open('inventory_data.csv', 'w', newline='') as csvfile:
        cw = csv.writer(csvfile)
        cw.writerow(productInfo)

        for item in item_list:
            nextRow = []
            nextRow.append(item.id)
            nextRow.append(item.title) 
            nextRow.append(item.stock) 
            nextRow.append(item.status.replace('-', ' '))
            nextRow.append("" if item.price == None else "$" + str(item.price))
            nextRow.append(item.date)
            nextRow.append(item.description)

            cw.writerow(nextRow)
    
    return send_file('inventory_data.csv',
                     mimetype='text/csv',
                     attachment_filename='inventory_data.csv',
                     as_attachment=True) 


if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", port="9832", debug=True)




