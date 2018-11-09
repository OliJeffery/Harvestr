import mysql.connector
import json

class Database:

	def __init__(self):
		with open('mysql_credentials.json') as mysql_credentials:
			json_credentials = json.loads(mysql_credentials.read())
			self.connection = mysql.connector.connect(
			  		host=json_credentials['host'],
			  		user=json_credentials['user'],
			  		passwd=json_credentials['passwd'],
			  		database=json_credentials['database']
				)

if __name__ == '__main__':
	database = Database()
	connection = database.connect()
	print(
			connection.get_rows(
				connection.cmd_query(
					'SELECT * FROM `users`'
					)
				)[0]
			)
		
