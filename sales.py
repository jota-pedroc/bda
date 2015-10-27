from random import randint
from client import load_persons
from product import load_products




def order_from_client_city(client, cities):
	"""get a order id corresponding to the client's city"""
	city_id = cities.index(client.city)
	return city_id*2 + randint(0,1)

#([quantiade], [valor], [taxa_entrega], [tempo_fk], [funcionario_id], [cliente_id], [pedido_id], [produto_id], [desconto])

def generate_sale(products, persons, cities):
	# 1. pick a establishment (pick a neighborhood)

	# 2. pick a client from the same city

	# 3. pick a list of products and quantity of products

	# 4. pick a payment method

	# 5. pick a time

	# 6. pick an employee from that establishment

	# 7. generate an order

	# 8. generate a sale for each product (all refering to the same order)


	#lista de produtos




	product = randint(0, len(products)-1) # select one product among the loaded products

	quantity = randint(1,5) # random quantity between 1 and 5

	price = float(products[product].price) * quantity # sale price = product price * quantity

	delivery = randint(5,10) # random delivery fee between 5 and 10

	time = randint(1414331506, 1445867507) # random time from 26/10/2014 untill 26/10/2015

	employee = randint(1, 11) # random employee id

	client = persons[randint(1, len(persons)-1)] # select a client among the loaded clients

	order = order_from_client_city(client, cities) # get a order id corresponding to the client city

	discount = 0 # no discounts are currently being given

	return ("INSERT INTO [dbo].[Venda] ([quantidade], [valor], [taxa_entrega], [tempo_fk], [funcionario_id], [cliente_id], [pedido_id], [produto_id], [desconto])"+
			" VALUES ({!s}, CAST('${:.2f}' AS MONEY),CAST('${:.2f}' AS MONEY),'{}','{}','{}','{}','{}','{}');").format(quantity, price, delivery, time, employee, client.id, order, product, discount)

def main():
	#---------------------INPUT--------------------------------
	products = load_products('products.sql')
	persons = load_persons('clients.sql')
	cities = [line.rstrip('\n') for line in open('cities.txt')]

	#--------------EXECUTION AND OUTPUT------------------------
	n_sales = 50
	sql_sales_file = open("sales.sql", "w")
	for i in range(n_sales):
		sql_sales_file.write(generate_sale(products, persons, cities) + "\n")
	sql_sales_file.close()
		