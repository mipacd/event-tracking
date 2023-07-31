# Event Tracking API Application

This application uses Postgres and Flask to provide endpoints for viewing and modifying event data using JSON objects. By default, the application creates a table named "events" in the default "postgres" database upon launch. This table has an automatically incrementing primary key as the id, an automatic timestamp, and a metric and value provided by the client. The table is automatically removed when the application is closed using CTRL+C (SIGTERM).

## Installation

1. Checkout code with git or download from Github
2. Ensure Flask and psycopg2 Python packages are installed. If not, run:
`pip install -r requirements.txt`
3. Modify the PG_* variables at the top of run.py to set Postgres connection parameters
4. Run the application:
`python3 run.py`

## Endpoints with Examples

### POST /create
Add an event to the table. All parameters are required.

Query Parameters:
- metric: string
- value: decimal

Response Parameters:
- success: bool

Response:
- success = True, HTTP 200 on success. success= False, HTTP 400 on fail

Query Examples:  
`curl -X POST http://localhost:3000/create -H 'Content-Type: application/json' -d '{"metric": "CPU_UTIL", "value": 70}'`

`curl -X POST http://localhost:3000/create -H 'Content-Type: application/json' -d '{"metric": "MEM_UTIL", "value": 45}'`

### GET /list
List all events in the table.

Query Parameters:
- None

Response:
- JSON object with list of events, empty object with HTTP 400 on fail

Query Example:  
`curl -X GET http://localhost:3000/list -H 'Content-Type: application/json'`

### GET /view
View the event for a given id. All parameters are required.

Query Parameters:
- id: int

Response:
- JSON object with event, empty object with HTTP 400 on fail

Query Example:
`curl -X GET http://localhost:3000/view -H 'Content-Type: application/json' -d '{"id": 2}'`

### DELETE /remove
Remove the event for a given id. All parameters are required.

Query Parameters:
- id: int

Response Parameters:
- success: bool

Response:
- success = True, HTTP 200 on success. success= False, HTTP 400 on fail

Query Example:  
`curl -X DELETE http://localhost:3000/remove -H 'Content-Type: application/json' -d '{"id": 2}'`

### GET /search
Search metric values for a given substring. Case insensitive. All parameters are required.

Query Parameters:
- metric: string

Response:
- JSON object with event, empty object with HTTP 400 on fail

Query Example:  
`curl -X GET http://localhost:3000/search -H 'Content-Type: application/json' -d '{"metric": "cpu"}'`

