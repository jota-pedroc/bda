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
		return ("INSERT INTO [dbo].[Funcionario] ([funcionario_id], [funcionario_nome], [sexo], [telefone], [cpf], [salario])"+
			" VALUES ({!s},'{}','{}','{}','{}',CAST('${}' AS MONEY));").format(self.id, self.name, self.sex, self.phone, self.cpf, self.payment)

	
	@staticmethod
	def employee_from_insert_stmnt(stmnt):
		values = stmnt.find("VALUES")
		first_arg = stmnt.find('(', values)
		end = stmnt.find(')', values)
		args = stmnt[first_arg+1:end].split(',')
		for idx, val in enumerate(args):
			args[idx] = val.strip('\'')
		return Employee(*args)



#-----------------AUXILIARY FUNCTIONS-----------------------

def load_employee(file_path):
	"""Given a file path to a sql file with enployee insert statements, return me the python list of corresponding Enployee instances"""
	employees = []
	for line in open(file_path):
		employee = Enployee.enployee_from_insert_stmnt(line)
		employees.append(employee)
	return employees

#-----------------------GENERATOR---------------------------
def generate_employees(maleNames, femaleNames, amount):
	n_maleNames = len(maleNames)
	n_femaleNames = len(femaleNames)

	maleNames = maleNames[:amount]
	femaleNames = femaleNames[:amount]

	employees = []
	employee_id = 1
	sexes = [0, 1]
	phone_id = 0
	cpf_id  = 0
	payment = 2000.00

	for name in maleNames:
		sex = sexes[0]

		phone = str(phone_id).zfill(8)
		phone = phone[:4] + '-' + phone[4:]

		cpf = str(cpf_id).zfill(11)
		cpf = cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:]

		singlePayment = payment + randint(100, 1100)

		employee = Employee(employee_id, name, sex, phone, cpf, singlePayment)
		employees.append(employee)

		employee_id += 1
		phone_id += 1
		cpf_id += 1

	for name in femaleNames:
		sex = sexes[1]

		phone = str(phone_id).zfill(8)
		phone = phone[:4] + '-' + phone[4:]

		cpf = str(cpf_id).zfill(11)
		cpf = cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:]

		singlePayment = payment + randint(100, 1100)

		employee = Employee(employee_id, name, sex, phone, cpf, singlePayment)
		employees.append(employee)

		employee_id += 1
		phone_id += 1
		cpf_id += 1

	return employees


#-------------------------ACTUAL SCRIPT-----------------------

def main():

	#----------------------INPUT--------------------------------
	
	maleNames = [line.rstrip('\n') for line in open('employeeMaleNames.txt')]
	femaleNames = [line.rstrip('\n') for line in open('employeeFemaleNames.txt')]
	cities = [line.rstrip('\n') for line in open('cities.txt')]
	neighborhoods = [line.rstrip('\n') for line in open('neighborhoods.txt')]

	#--------------------EXECUTION--------------------------
	employees = generate_employees(maleNames, femaleNames, 15)

	#--------------------------OUTPUT-------------------------------
	count = {}
	sql_employees_file = open("enployees.sql", "w")
	for employee in employees:
		#print person
		#print person.insertStmnt()	
		sql_employees_file.write(employee.insertStmnt() + "\n")


	#------------------STATS REPORTING----------------------
	for key in count:
		n_maleNames = len(maleNames)
		n_femaleNames = len(femaleNames)
		print key+':' + str(count[key]) + ' - ' + str((count[key]/(n_names+0.0)))



