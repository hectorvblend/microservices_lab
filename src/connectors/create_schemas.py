from src.connectors.jobs import Job
from src.connectors.departments import Department
from src.connectors.hired_employees import HiredEmployees

ALLOWED_ENTITIES = {
	'jobs':Job,
	'departments':Department,
	'hiredEmployees': HiredEmployees
	}

def create_all_schemas():
	Job.__create_all_schemas__()
	HiredEmployees.__create_all_schemas__()
	Department.__create_all_schemas__()