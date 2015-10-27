from random import randint

#given a list of names, cities and neigborhoods, generate a client table.

#------------------------MODEL------------------------------
#([cliente_id], [nome], [sexo], [telefone], [cpf], [cidade_nome], [cidade_bairro_nome], [cidade_bairro_cep])
class Person:
	def __init__(self, id, name, sex, phone, cpf, city, neighborhood, zip_s):
		self.id = id
		self.name = name
		self.sex =  sex
		self.phone = phone
		self.cpf = cpf
		self.city = city
		self.neighborhood = neighborhood
		self.zip = zip_s
	def __str__(self):
		return '(' + self.name + '-' + self.city + '-'+self.neighborhood + ')'

	def insertStmnt(self):
		return ("INSERT INTO [dbo].[Cliente] ([cliente_id], [nome], [sexo], [telefone], [cpf], [cidade_nome], [cidade_bairro_nome], [cidade_bairro_cep])"+
			" VALUES ({!s},'{}','{}','{}','{}','{}','{}','{}');").format(self.id, self.name, self.sex, self.phone, self.cpf, self.city, self.neighborhood, self.zip)

	
	@staticmethod
	def person_from_insert_stmnt(stmnt):
		if 'INSERT' not in stmnt:
			return None
		values = stmnt.find("VALUES")
		first_arg = stmnt.find('(', values)
		end = stmnt.find(')', values)
		args = stmnt[first_arg+1:end].split(',')
		for idx, val in enumerate(args):
			args[idx] = val.strip('\'')
		return Person(*args)



#-----------------AUXILIARY FUNCTIONS-----------------------

def ngbhd_from_city(city_id, cities, neighborhoods):
	"""Given a city, return me a neighborhood from that city"""
	ngbhd_per_cty = len(neighborhoods)/len(cities)
	return randint(city_id*ngbhd_per_cty,(city_id*ngbhd_per_cty)+ngbhd_per_cty-1)

def load_persons(file_path):
	"""Given a file path to a sql file with client insert statements, return me the python list of corresponding Person instances"""
	persons = []
	for line in open(file_path):
		person = Person.person_from_insert_stmnt(line)
		if person:
			persons.append(person)
	return persons

#-----------------------GENERATOR---------------------------
def generate_persons(names, cities, neighborhoods):
	n_names = len(names)
	n_cities = len(cities)
	n_ngbhd = len(neighborhoods)
	

	persons = []
	sexes = ['M', 'F']
	person_id = 1
	phone_id = 0
	cpf_id  = 0 
	for name in names:
		sex = sexes[randint(0,len(sexes)-1)]

		phone = str(phone_id).zfill(8)
		phone = phone[:4] + '-' + phone[4:]

		cpf = str(cpf_id).zfill(11)
		cpf = cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:]

		city_id = randint(0, n_cities - 1)
		city = cities[city_id]

		ngbhd_id = ngbhd_from_city(city_id, cities, neighborhoods)
		ngbhd = neighborhoods[ngbhd_id]

		zip_s = str(city_id).zfill(5) + str(ngbhd_id).zfill(3)
		zip_s = zip_s[:5] + '-' + zip_s[5:]

		person = Person(person_id, name, sex, phone, cpf, city, ngbhd, zip_s)
		persons.append(person)

		person_id += 1
		phone_id += 1
		cpf_id += 1

	return persons


#-------------------------ACTUAL SCRIPT-----------------------

def main():

	#----------------------INPUT--------------------------------
	names = [line.rstrip('\n') for line in open('names.txt')]
	cities = [line.rstrip('\n') for line in open('cities.txt')]
	neighborhoods = [line.rstrip('\n') for line in open('neighborhoods.txt')]

	#--------------------EXECUTION--------------------------
	persons = generate_persons(names, cities, neighborhoods)

	#--------------------------OUTPUT-------------------------------
	# count = {}
	sql_clients_file = open("clients.sql", "w")
	sql_clients_file.write("USE [lolbibis]\nGO\n\n")
	for person in persons:
		#print person
		#print person.insertStmnt()	
		sql_clients_file.write(person.insertStmnt() + "\n")

		#-------------STATS GATHERING---------------
		# if not (person.city in count):
		# 	count[person.city] = 0
		# count[person.city] = count[person.city] + 1
	sql_clients_file.write("GO\n\n")
	sql_clients_file.close()

	#------------------STATS REPORTING----------------------
	# for key in count:
	# 	n_names = len(names)
	# 	print key+':' + str(count[key]) + ' - ' + str((count[key]/(n_names+0.0)))



