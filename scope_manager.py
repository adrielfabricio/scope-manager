import os
import re
import argparse

class ScopeManager:
	"""
	A class that manages scopes and tokens in a programming language.

	Attributes:
		regex_whitespace (str): Regular expression pattern for matching whitespace.
		regex_number (str): Regular expression pattern for matching numbers.
		regex_variable_number (str): Regular expression pattern for matching variable assignments with numbers.
		regex_string (str): Regular expression pattern for matching strings.
		regex_variable_string (str): Regular expression pattern for matching variable assignments with strings.
		regex_variable (str): Regular expression pattern for matching variable assignments.
		regex_print (str): Regular expression pattern fsor matching print statements.
		regex_declared_number (str): Regular expression pattern for matching declared numbers.
		regex_undeclared_number (str): Regular expression pattern for matching undeclared numbers.
		regex_declared_string (str): Regular expression pattern for matching declared strings.
		regex_undeclared_string (str): Regular expression pattern for matching undeclared strings.
		scopes (list): A list of scopes.
		block_identifiers (list): A list of block identifiers.

	Methods:
		get_token_by_identifier(identifier): Returns the token with the given identifier.
		variable_exists(identifier, scope): Checks if a variable with the given identifier exists in the scope.
		assign_value_to_token(identifier, value): Assigns a value to the token with the given identifier.
		process_line(line): Processes a single line of code.
		process_scope(file_path): Processes the code in the specified file path.
	"""
	def __init__(self):
		self.regex_whitespace = r"\s+"
		self.regex_number = r"[+-]?\d+(\.\d+)?"
		self.regex_variable_number = r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*" + self.regex_number
		self.regex_string = r'"([^"]*)"'
		self.regex_variable_string = r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*" + self.regex_string
		self.regex_variable = r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[a-zA-Z_][a-zA-Z0-9_]*"
		self.regex_print = r"PRINT\s+[a-zA-Z_][a-zA-Z0-9_]*"
		self.regex_declared_number = f"NUMERO{self.regex_whitespace}{self.regex_variable_number}"
		self.regex_undeclared_number = r"NUMERO\s+[a-zA-Z_][a-zA-Z0-9_]*"
		self.regex_declared_string = f"CADEIA{self.regex_whitespace}{self.regex_variable_string}"
		self.regex_undeclared_string = r"CADEIA\s+[a-zA-Z_][a-zA-Z0-9_]*"

		self.scopes = []
		self.output_lines = []
		self.block_identifiers = []

	def get_token_by_identifier(self, identifier):
		"""
		Returns the token with the given identifier.

		Args:
			identifier (str): The identifier of the token.

		Returns:
			list or None: The token with the given identifier, or None if not found.
		"""
		for scope in reversed(self.scopes):
			for current_token in scope:
				if current_token[2] == identifier:
						return current_token
		return None

	def variable_exists(self, identifier, scope):
		"""
		Checks if a variable with the given identifier exists in the scope.

		Args:
			identifier (str): The identifier of the variable.
			scope (list): The scope to search in.

		Returns:
			bool: True if the variable exists, False otherwise.
		"""
		return any(current_token[2] == identifier for current_token in scope)

	def assign_value_to_token(self, identifier, value):
		"""
		Assigns a value to the token with the given identifier.

		Args:
			identifier (str): The identifier of the token.
			value: The value to assign.
		"""
		for scope in reversed(self.scopes):
			for current_token in scope:
				if current_token[2] == identifier:
					current_token[3] = value
					return None

	def process_line(self, line, line_number):
		"""
		Processes a single line of code.

		Args:
			line (str): The line of code to process.
   		line_number (int): The line number of the code.
		"""
		line = line.strip().replace("\n", "")
		if "BLOCO" in line:
			self.block_identifiers.append(line.split(" ")[-1])
			self.scopes.append([])
			self.output_lines.append(f'\n{"*INICIO " + self.block_identifiers[-1] + "*"}')
		elif self.block_identifiers and re.match(f"FIM{self.regex_whitespace}{self.block_identifiers[-1]}", line):
			if self.scopes:
				self.scopes.pop()
				self.output_lines.append(f'\n{"*FIM " + self.block_identifiers[-1] + "*"}')
				self.block_identifiers.pop()
		elif re.match(self.regex_declared_string, line) or re.match(self.regex_declared_number, line):
			if "," in line:
				var_type, *rest = line.split(" ", 1)
				assignments = map(str.strip, rest[0].split(","))
				for assignment in assignments:
					id_current, *value = map(str.strip, assignment.split("="))
					if not self.variable_exists(id_current, self.scopes[-1]):
						self.scopes[-1].append(["tk_identificador", var_type, id_current, value[0] if value else "0"])
			else:
				var_type, *rest = line.split(" ", 1)
				id_unique, *value = map(str.strip, rest[0].split("="))
				if not self.variable_exists(id_unique, self.scopes[-1]):
					self.scopes[-1].append(["tk_identificador", var_type, id_unique, value[0] if value else "0"])
		elif re.match(self.regex_undeclared_string, line) or re.match(self.regex_undeclared_number, line):
			var_type, id_unique = map(str.strip, line.split(" "))
			if not self.variable_exists(id_unique, self.scopes[-1]):
				self.scopes[-1].append(["tk_identificador", var_type, id_unique, "0"])
		elif re.match(self.regex_variable, line):
			id_a, *id_b = map(str.strip, line.split("="))
			token_b = self.get_token_by_identifier(id_b[0])
			if token_b is None:
				self.output_lines.append(f"Linha {line_number}: {id_b[0]} não declarado")
				return
			token_a = self.get_token_by_identifier(id_a)
			if token_a is None:
				self.scopes[-1].append(["tk_identificador", token_b[1], id_a, token_b[3]])
			else:
				if token_a[1] == token_b[1]:
					self.assign_value_to_token(id_a, token_b[3])
				else:
					self.output_lines.append(f"Linha {line_number}: {id_a} : Atribuição inválida")
		elif re.match(self.regex_variable_number, line) or re.match(self.regex_variable_string, line):
			id_a, value_a = map(str.strip, line.split("="))
			token = self.get_token_by_identifier(id_a)
			if token is None:
				if re.match(self.regex_number, value_a):
					self.scopes[-1].append(["tk_identificador", "NUMERO", id_a, value_a])
				elif re.match(self.regex_string, value_a):
					self.scopes[-1].append(["tk_identificador", "CADEIA", id_a, value_a])
				else:
					self.output_lines.append(f"Linha {line_number}: Error: Valor ou cadeia inválida.")
			else:
				if token[1] == "NUMERO" and re.match(self.regex_number, value_a):
					self.assign_value_to_token(id_a, value_a)
				elif token[1] == "CADEIA" and re.match(self.regex_string, value_a):
					self.assign_value_to_token(id_a, value_a)
				else:
					self.output_lines.append(f"Linha {line_number}: {id_a} : Atribuição inválida")
		elif re.match(self.regex_print, line):
			id_a = line.split(" ")[-1]
			token = self.get_token_by_identifier(id_a)
			if token is None:
				self.output_lines.append(f"Linha {line_number}: {id_a} não declarado")
			else:
				self.output_lines.append(f"{id_a} = {token[3]} em {self.block_identifiers[-1]}")

	def process_scope(self, file_path):
		"""
		Processes the code in the specified file path.

		Args:
			file_path (str): The path to the file containing the code.
		"""
		with open(file_path, "r") as file:
			lines = file.readlines()

		for line_number, line in enumerate(lines, 1):
			self.process_line(line, line_number)

		# Ensure the outputs directory exists
		output_dir = "outputs"
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)

		# Create the output file path
		input_file_name = os.path.basename(file_path)
		output_file_name = os.path.splitext(input_file_name)[0] + ".out"
		output_file_path = os.path.join(output_dir, output_file_name)

		with open(output_file_path, "w") as output_file:
			output_file.write("\n".join(self.output_lines))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Process a file with scope and type management.")
	parser.add_argument("file_path", help="The path to the file to be processed.")
	args = parser.parse_args()

	manager = ScopeManager()
	manager.process_scope(args.file_path)
