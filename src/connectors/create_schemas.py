from src.connectors.application_tables.jobs import Job
from src.connectors.application_tables.departments import Department
from src.connectors.application_tables.hired_employees import HiredEmployees
from src.connectors.long_process.async_process import AsyncProcess

ALLOWED_ENTITIES = {
	'jobs':Job,
	'departments':Department,
	'hiredEmployees': HiredEmployees,
	'asyncProcess': AsyncProcess
	}

def create_all_schemas():
	Job.__create_all_schemas__()
	HiredEmployees.__create_all_schemas__()
	Department.__create_all_schemas__()
	AsyncProcess.__create_all_schemas__()