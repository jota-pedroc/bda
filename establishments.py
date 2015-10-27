class Establishment:
	def __init__(self, city, neighborhood, zip_code, name, cnpj, phone):
		self.city = city
		self.neighborhood = neighborhood
		self.zip_code = zip_code
		self.name = name
		self.cnpj = cnpj
		self.phone = phone




def load_establishments(cities_file_path, neighborhoods_file_path):
	cities = [line.rstrip('\n') for line in open('cities.txt')]
	neighborhoods = [line.rstrip('\n') for line in open('neighborhoods.txt')]

	for i in range(len(cities)*3):
		