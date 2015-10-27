from random import randint

#given a list of names, cities and neigborhoods, generate a client table.

#------------------------MODEL------------------------------
#([cliente_id], [nome], [sexo], [telefone], [cpf], [cidade_nome], [cidade_bairro_nome], [cidade_bairro_cep])
class Employee:
	def __init__(self, id, name ,sex, phone, cpf, payment):
		self.id = id
		self.name = name
		self.sex =  sex
		self.phone = phone
		self.cpf = cpf
		self.payment = payment

	def __str__(self):
		return '(' + self.name + '-' + self.cpf + ')'

	def insertStmnt(self):
		return ("INSERT INTO [dbo].[Funcionario] ([funcionario], [nome], [sexo], [telefone], [cpf], [salario])"+
			" VALUES ({!s},'{}','{}','{}','{}','{}', CAST('${}' AS MONEY));").format(self.id, self.name, self.birthday, self.sex, self.phone, self.cpf, self.payment)

	
	@staticmethod
	def enployee_from_insert_stmnt(stmnt):
		values = stmnt.find("VALUES")
		first_arg = stmnt.find('(', values)
		end = stmnt.find(')', values)
		args = stmnt[first_arg+1:end].split(',')
		for idx, val in enumerate(args):
			args[idx] = val.strip('\'')
		return Enployee(*args)



#-----------------AUXILIARY FUNCTIONS-----------------------

def load_enployee(file_path):
	"""Given a file path to a sql file with enployee insert statements, return me the python list of corresponding Enployee instances"""
	enployees = []
	for line in open(file_path):
		enployee = Enployee.enployee_from_insert_stmnt(line)
		enployees.append(enployee)
	return enployees

#-----------------------GENERATOR---------------------------
def generate_enployees(names):
	n_names = len(names)
	#n_cities = len(cities)
	#n_ngbhd = len(neighborhoods)
	

	enployees = []
	enployee_id = 1
	sexes = [0, 1]
	phone_id = 0
	cpf_id  = 0
	payment = 2000.00
	for name in names:
		sex = sexes[randint(0,len(sexes)-1)]

		phone = str(phone_id).zfill(8)
		phone = phone[:4] + '-' + phone[4:]

		cpf = str(cpf_id).zfill(11)
		cpf = cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:]

		singlePayment = payment + randint(100, 1100)

		enployee = Enployee(person_id, name, sex, phone, cpf, singlePayment)
		enployees.append(enployee)

		enployee_id += 1
		phone_id += 1
		cpf_id += 1

	return enployees


#-------------------------ACTUAL SCRIPT-----------------------

def main():

	#----------------------INPUT--------------------------------
	names = [line.rstrip('\n') for line in open('names.txt')]
	cities = [line.rstrip('\n') for line in open('cities.txt')]
	neighborhoods = [line.rstrip('\n') for line in open('neighborhoods.txt')]

	#--------------------EXECUTION--------------------------
	persons = generate_persons(names, cities, neighborhoods)

	#--------------------------OUTPUT-------------------------------
	count = {}
	sql_clients_file = open("clients.sql", "w")
	for person in persons:
		#print person
		#print person.insertStmnt()	
		sql_clients_file.write(person.insertStmnt() + "\n")

		#-------------STATS GATHERING---------------
		if not (person.city in count):
			count[person.city] = 0
		count[person.city] = count[person.city] + 1
	sql_clients_file.close()

	#------------------STATS REPORTING----------------------
	for key in count:
		n_names = len(names)
		print key+':' + str(count[key]) + ' - ' + str((count[key]/(n_names+0.0)))



