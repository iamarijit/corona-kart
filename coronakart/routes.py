from coronakart import app
from flask import render_template, url_for, request
import json

def get_items():
	with open('coronakart\items.json') as items_file:
		items = json.load(items_file)
		return items

def update_items(items):
	with open('coronakart\items.json', 'w') as items_file: 
		json.dump(items, items_file, indent=4)

def get_item_by_id(id):
	items = get_items()
	selected = [i for i in items if i["id"]==id][0]
	return selected

def update_items_by_id(id, key, value):
	items = get_items()

	for index in range(len(items)):
		if items[index]["id"] == id:
			items[index][key] = value
			break

	update_items(items)

@app.route("/")
@app.route("/kart")
def kart():
	items = get_items()
	return render_template("kart.html", items=items)

@app.route("/order/<string:id>")
def order(id):
	item = get_item_by_id(id)
	return render_template("order.html", item=item)

@app.route("/placed/<string:id>", methods=['GET', 'POST'])
def placed(id):
	item = get_item_by_id(id)
	order = request.form

	quantity = int(order["quantity"].strip())
	price = quantity * item['price']
	update_items_by_id(id, "available", item["available"] - quantity)
	
	return render_template("placed.html", item=item, order=order, price=price)