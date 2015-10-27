#INSERT INTO [dbo].[Produto] ([produto_id], [nome], [preco_venda], [custo_compra], [tamanho], [categoria_nome], [categoria_descricao], [produto_descricao], [produto_marca])
	#VALUES (7,'Pizza de Frango com Catupiry',CAST('$20.00' AS MONEY),CAST('$10.00' AS MONEY),'grande','pizza','pizza com massa grossa','frango desfiado','pizza');
class Product:
	def __init__(self, id, name, price, cost, size, category, category_description, description, brand):
		self.id = id
		self.name = name
		self.price = price
		self.cost = cost
		self.size = size
		self.category = category
		self.category_description = category_description
		self.description = description
		self.brand = brand

	def insert_stmnt(se):
		return "INSERT INTO [dbo].[Produto] ([produto_id], [nome], [preco_venda], [custo_compra], [tamanho], [categoria_nome], [categoria_descricao], [produto_descricao], [produto_marca])" + " VALUES ({},{},CAST('${}' AS MONEY),CAST('${}' AS MONEY),'{}','{}','{}','{}','{}');".format(self.id, self.price, self.cost, self.size, self.category, self.category_description, self.brand)

	@staticmethod
	def product_from_insert_stmnt(stmnt):
		if not stmnt.strip() or 'GO' in stmnt:
			return None
		values = stmnt.find("VALUES")
		first_arg = stmnt.find('(', values)
		args = stmnt[first_arg:].split(',')
		for idx, val in enumerate(args):
			if isinstance(val, str) and 'CAST' in val:
				start = val.find('$')
				end = val.find('\'', start)
				args[idx] = float(val[start+1:end])
			else:
				args[idx] = val.strip('\'();')
		return Product(*args)


def load_products(file_path):
	products = []
	for line in open(file_path):
		product = Product.product_from_insert_stmnt(line)
		if product:
			products.append(product)
	return products
		