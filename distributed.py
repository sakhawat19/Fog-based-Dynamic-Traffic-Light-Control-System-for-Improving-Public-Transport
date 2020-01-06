#!/usr/bin/python
import MySQLdb
import datetime


# db = MySQLdb.connect(host="MYSQL5014.site4now.net",  # your host 
#                      user="9b464c_edtlc",       # username
#                      passwd="db_9b464c",     # password
#                      db="db_9b464c_edtlc")   # name of the database
 

host = "172.21.0.1"
port = 3312         ### default mysql port, change if you know better
user = "root"      ### def parameters
passwd = "password"     ### def parameters
db = "pydocker"      ### connection.user_info contains the autho users

### Create a connection object, use it to create a cursor

con = MySQLdb.connect(host = host  ,port = port , user = user,passwd = passwd ,db = db)




# Create a Cursor object to execute queries.
# cur = db.cursor()
cur = con.cursor()


def fetchNeiberingImpact(int_id, int_lane_id):
	# Select data from table using SQL query.
	cur.execute("SELECT status, last_update FROM `traffic_data_current` WHERE int_id = %s and int_lane_id = %s ORDER by id DESC limit 1", (int_id, int_lane_id))

	# print the first and second columns      
	#for row in cur.fetchall() :
	#    print row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4]

	rows = cur.fetchall()
	return rows

def fetchDependency(intID, int_lane):
	
	# Select data from table using SQL query.
	cur.execute("SELECT * FROM `lane_dependency` WHERE `dep_int_id` = %s AND `dep_int_lane_id` = %s", (intID, int_lane))

	rows = cur.fetchall()
	return rows

def insertDt(int_id, int_lane_id, status):
	nowTimeStamp = datetime.datetime.now()
	
	cur.execute("INSERT INTO traffic_data_current (int_id, int_lane_id, status, last_update) VALUES (%s, %s, %s, %s)",(int_id, int_lane_id, status, nowTimeStamp))

	
def fetchNeiberingImpact2(int_id, int_lane_id):
	# Select data from table using SQL query.
	cur.execute("SELECT status, last_update FROM `traffic_data_current2` WHERE int_id = %s and int_lane_id = %s ORDER by id DESC limit 1", (int_id, int_lane_id))

	# print the first and second columns      
	#for row in cur.fetchall() :
	#    print row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4]

	rows = cur.fetchall()
	return rows

def fetchDependency2(intID, int_lane):
	
	# Select data from table using SQL query.
	cur.execute("SELECT * FROM `lane_dependency2` WHERE `dep_int_id` = %s AND `dep_int_lane_id` = %s", (intID, int_lane))

	rows = cur.fetchall()
	return rows

def insertDt2(int_id, int_lane_id, status):
	nowTimeStamp = datetime.datetime.now()
	
	cur.execute("INSERT INTO traffic_data_current2 (int_id, int_lane_id, status, last_update) VALUES (%s, %s, %s, %s)",(int_id, int_lane_id, status, nowTimeStamp))
