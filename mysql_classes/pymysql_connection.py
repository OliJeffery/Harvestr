import json
import os
import pymysql

class Database:

	def query(self, sql):
		try:
			with open('mysql_credentials.json') as mysql_credentials:
				json_credentials = json.loads(mysql_credentials.read())
				db_connection_name = json_credentials['host']
				db_user = json_credentials['user']
				db_password = json_credentials['passwd']
				db_name = json_credentials['database']
				if os.environ.get('GAE_ENV') == 'standard':
					# If deployed, use the local socket interface for accessing Cloud SQL
					unix_socket = '/cloudsql/{}'.format(db_connection_name)
					cnx = pymysql.connect(user=db_user, password=db_password,
										  unix_socket=unix_socket, db=db_name)
				else:
					# If running locally, use the TCP connections instead
					# Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
					# so that your application can use 127.0.0.1:3306 to connect to your
					# Cloud SQL instance
					host = '127.0.0.1'
					cnx = pymysql.connect(user=db_user, password=db_password,
										  host=host, db=db_name)
				with cnx.cursor(pymysql.cursors.DictCursor) as cursor:
					cursor.execute(sql)
					result = cursor.fetchall()
				cnx.close()

				return result
			
		except Exception as error:
			self.report_error()

	def update(self, query, args):
		try:
			with open('mysql_credentials.json') as mysql_credentials:
				json_credentials = json.loads(mysql_credentials.read())
				db_connection_name = json_credentials['host']
				db_user = json_credentials['user']
				db_password = json_credentials['passwd']
				db_name = json_credentials['database']
				if os.environ.get('GAE_ENV') == 'standard':
					# If deployed, use the local socket interface for accessing Cloud SQL
					unix_socket = '/cloudsql/{}'.format(db_connection_name)
					cnx = pymysql.connect(user=db_user, password=db_password,
										  unix_socket=unix_socket, db=db_name)
				else:
					# If running locally, use the TCP connections instead
					# Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
					# so that your application can use 127.0.0.1:3306 to connect to your
					# Cloud SQL instance
					host = '127.0.0.1'
					cnx = pymysql.connect(user=db_user, password=db_password,
										  host=host, db=db_name)
				with cnx.cursor() as cursor:
					cursor.execute(query, args)
					cnx.commit()

				cnx.close()

				return str(result)
			
		except Exception as error:
			self.report_error(error)		 

	def report_error(self, error):
		print(f"ERROR: {error}")

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
		
