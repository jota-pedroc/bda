from random import randint
from client import load_persons
from product import load_products
from establishment import create_establishments
from Employee import load_employees
import datetime




def order_from_client_city(client, cities):
	"""get a order id corresponding to the client's city"""
	city_id = cities.index(client.city)
	return city_id*2 + randint(0,1)

#([quantiade], [valor], [taxa_entrega], [tempo_fk], [funcionario_id], [cliente_id], [pedido_id], [produto_id], [desconto])

def get_cities_to_clients(client_list):
	dic = {}
	for client in client_list:
		if client.city not in dic:
			dic[client.city] = []
		dic[client.city].append(client)
	return dic

def generate_sales(n_sales, establishments, cities_to_clients, products, employees):
	payment_methods = ['cartao', 'dinheiro']
	order_id = 1
	orders = []	
	sales = []
	for n in range(n_sales):
		# 1. pick a establishment (pick a neighborhood)
		establishment = establishments[randint(0,len(establishments)-1)]

		# 2. pick a client from the same city
		city = establishment.city
		possible_clients = cities_to_clients[city]
		client = possible_clients[randint(0, len(possible_clients)-1)]

		# 3. pick a list of products and quantity of products
		n_products = randint(1,5)
		selected_products = []
		product_quantity = []
		for i in range(n_products):
			product = products[randint(0, len(products)-1)]
			selected_products.append(product)
			product_quantity.append(randint(1,5))

		# 4. pick a payment method
		payment_method = payment_methods[randint(0, len(payment_methods)-1)]

		# 5. pick a time
		time = randint(1325469526, 1445867507) 
		date = datetime.datetime.fromtimestamp(time)
		time = str(date) + '.000'

		# 6. pick an employee from that establishment
		employee = employees[randint(0, len(employees)-1)]

		# 7. generate an order
		order = "INSERT INTO [dbo].[Pedido] ([pedido_id],[forma_pagamento], [cidade_nome], [cidade_bairro_nome], [cidade_bairro_cep], [cidade_bairro_estabelecimento_nome], [cidade_bairro_estabelecimento_cnpj], [cidade_bairro_estabelecimento_telefone])" + " VALUES ({},'{}', '{}','{}','{}', '{}','{}','{}');".format(order_id, payment_method, establishment.city, establishment.neighborhood, establishment.zip, establishment.name, establishment.cnpj, establishment.phone)
		orders.append(order)

		# 8. generate a sale for each product (all refering to the same order)
		discount = 0
		delivery = randint(5,10)		
		for idx, product in enumerate(selected_products):
			quantity = product_quantity[idx]
			sale = ("INSERT INTO [dbo].[Venda] ([quantidade], [valor], [taxa_entrega], [tempo_fk], [funcionario_id], [cliente_id], [pedido_id], [produto_id], [desconto])" + 
				" VALUES ({!s}, CAST('${:.2f}' AS MONEY),CAST('${:.2f}' AS MONEY),'{}',{},{},{},{},{});").format(
					quantity, 
					product.price*quantity, 
					delivery, 
					time, 
					employee.id, 
					client.id, 
					order_id, 
					product.id, 
					discount)
			sales.append(sale)

		order_id += 1
	return (orders, sales)

def main():
	#---------------------INPUT--------------------------------	
	establishments = create_establishments('cities.txt', 'neighborhoods.txt')
	persons = load_persons('clients.sql')
	products = load_products('products.sql')
	employees = load_employees('employees.sql')
	n_orders = 5000
	#-------------------EXECUTION------------------------------
	cities_to_clients = get_cities_to_clients(persons)
	(orders, sales) = generate_sales(n_orders, establishments, cities_to_clients, products, employees)


	#--------------------OUTPUT--------------------------------
	sql_orders_file = open("orders.sql", "w")
	for line in orders:
		sql_orders_file.write(line + "\n")
	sql_orders_file.write('GO\n\n')
	sql_orders_file.close()

	sql_sales_file = open("sales.sql", "w")
	for line in sales:
		sql_sales_file.write(line + "\n")
	sql_sales_file.write('GO\n\n')
	sql_sales_file.close()

		