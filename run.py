from flask import Flask, jsonify, request
import datetime
import json
import psycopg2
import signal
import sys

PG_HOST="localhost"
PG_PORT="5432"
PG_USER="postgres"
PG_PASS="admin"
PG_DB="postgres"

app = Flask(__name__)
	
def get_connection():
	return psycopg2.connect(database=PG_DB,
							user=PG_USER,
							password=PG_PASS,
							host=PG_HOST,
							port=PG_PORT)
							
def init():
	conn = get_connection()
	cur= conn.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS events (
					ID SERIAL PRIMARY KEY,
					CREATED_AT timestamp with time zone default current_timestamp,
					METRIC VARCHAR(40),
					VALUE DECIMAL
	);""")
	conn.commit()
	conn.close()
	
def cleanup(signal, frame):
	print("Cleaning up table")
	conn = get_connection()
	cur= conn.cursor()
	cur.execute("DROP TABLE IF EXISTS events")
	conn.commit()
	conn.close()
	print("Cleanup complete")
	sys.exit()
	
def format(cur):
	rows = cur.fetchall()
	cols = [desc[0] for desc in cur.description]
	result = []
	for row in rows:
		row = dict(zip(cols, row))
		result.append(row)
	return jsonify(result)

@app.route('/list')
def list():
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT * from events")
	
	return format(cur)

@app.route('/create', methods=['POST'])
def create():
	conn = get_connection()
	cur = conn.cursor()
	
	request_data = request.get_json()
	if "metric" not in request_data or "value" not in request_data:
		return jsonify([]), 400
	metric = request_data['metric']
	value = request_data['value']
	try:
		cur.execute("INSERT INTO events (metric, value) VALUES (%s, %s)", (metric, value))
		conn.commit()
	except Exception as ex:
		return jsonify(success=False), 400
	
	return jsonify(success=True)
	
@app.route('/view')
def view():
	conn = get_connection()
	cur = conn.cursor()
	
	request_data = request.get_json()
	if "id" not in request_data:
		return jsonify([]), 400
	id = request_data['id']
	cur.execute("SELECT * from events WHERE id = %s", (id,))
	return format(cur)
	
@app.route('/remove', methods=['DELETE'])
def remove():
	conn = get_connection()
	cur = conn.cursor()
	
	request_data = request.get_json()
	if "id" not in request_data:
		return jsonify(success=False), 400
	id = request_data['id']
	try:
		cur.execute("DELETE from events WHERE id = %s", (id,))
		conn.commit()
	except Exception as ex:
		return jsonify(success=False), 400
		
	return jsonify(success=True)
	
@app.route('/search')
def search():
	conn = get_connection()
	cur = conn.cursor()
	
	request_data = request.get_json()
	if "metric" not in request_data:
		return jsonify([]), 400
	metric = request_data['metric']
	cur.execute(f"SELECT * from events WHERE metric ILIKE '%{metric}%'")
	
	return format(cur)
	
if __name__ == '__main__':
	init()
	signal.signal(signal.SIGINT, cleanup)
	app.run(port=3000)
	