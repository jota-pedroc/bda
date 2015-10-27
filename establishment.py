class Establishment:
	def __init__(self, city, neighborhood, zip_code, name, cnpj, phone):
		self.city = city
		self.neighborhood = neighborhood
		self.zip = zip_code
		self.name = name
		self.cnpj = cnpj
		self.phone = phone




def create_establishments(cities_file_path, neighborhoods_file_path):
	cities = [line.rstrip('\n') for line in open(cities_file_path)]
	neighborhoods = [line.rstrip('\n') for line in open(neighborhoods_file_path)]
	ngh_per_cty = len(neighborhoods)/len(cities)
	establishments = []
	for i in range(len(cities)):
		for j in range(3):
			new_esta = Establishment(cities[i], neighborhoods[i*ngh_per_cty + j], str(i).zfill(5) + '-' + str(j).zfill(3), 'lolbibs - ' + neighborhoods[i*ngh_per_cty + j], i*ngh_per_cty + j, str(i*ngh_per_cty + j).zfill(8))
			establishments.append(new_esta)

	return establishments

def test():
	estas = create_establishments('cities.txt', 'neighborhoods.txt')
	for aux in estas:
		print aux.name, aux.cnpj, aux.zip