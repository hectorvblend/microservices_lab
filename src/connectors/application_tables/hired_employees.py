import csv
from sqlalchemy import insert
from datetime import datetime
from src.connectors.application_tables.jobs import Job
from src.connectors.application_tables.departments import Department
from src.connectors.db_connect import ENGINE, BASE, SESSION, excecute
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, extract, asc, func, case, desc

class HiredEmployees(BASE):
    __tablename__ = 'hired_employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    datetime = Column(DateTime, default=datetime.utcnow)
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))

    @staticmethod
    def __delete_schema__():
        '''Delete table'''
        BASE.metadata.tables['hired_employees'].drop(ENGINE)

    @staticmethod
    def __create_all_schemas__():
        '''Create table'''
        BASE.metadata.create_all(ENGINE)


    @staticmethod
    async def insert_hired_employees(hired_employees: list):
        result = {'valids':[], 'invalids':[]}
        to_insert = []
        obj = {}
        for element in hired_employees:
            if element.id:
                obj['id'] = element.id
            if element.department_id:
                obj['department_id'] = element.department_id
            if element.job_id:
                obj['job_id'] = element.job_id
            obj['name'] = element.name
            try:
                stmt = insert(HiredEmployees).values(**obj).returning(HiredEmployees)
                query_result = excecute(stmt).fetchone()
                to_insert.append({
                    'id': int(query_result[0]),
                    'name': str(query_result[1]),
                    'datetime': str(query_result[2]),
                    'department_id': int(query_result[3]) if isinstance(query_result[3], int) else None,
                    'job_id': int(query_result[4]) if isinstance(query_result[4], int) else None
                    }
                )
            except Exception as e:
                    result['invalids'].append(obj)
            print(element)
        result['valids'] = to_insert
        return result

    @staticmethod
    async def instert_from_csv(file):
        result = {'valids':[], 'invalids':[]}
        f_content = await file.read()
        if file.filename.lower().endswith('.csv'):
            to_insert = []
            csvreaded = csv.reader(f_content.decode('utf-8').replace('\r\n', '\n').split('\n'))
            for element in csvreaded:
                if element != []:
                    try:
                        stmt = insert(HiredEmployees).values(
                            id= int(element[0]),
                            name= str(element[1]),
                            datetime= str(element[2]) if element[2] != '' else None,
                            department_id= int(element[3]) if element[3].isdigit() else None,
                            job_id= int(element[4]) if element[4].isdigit() else None
                            ).returning(HiredEmployees)
                        query_result = excecute(stmt).fetchone()
                        to_insert.append({
                            'id': int(query_result[0]),
                            'name': str(query_result[1]),
                            'datetime': str(query_result[2]),
                            'department_id': int(query_result[3]) if isinstance(query_result[3], int) else None,
                            'job_id': int(query_result[4]) if isinstance(query_result[4], int) else None
                            }
                        )
                    except Exception as e:
                            result['invalids'].append({
                            'id': element[0],
                            'name': element[1],
                            'datetime': element[2],
                            'department_id': element[3],
                            'job_id': element[4]
                            }
                        )
                    print(element)
        result['valids'] = to_insert
        return result

    @staticmethod
    async def get_by_quarter(year:int = 2021):
        session = SESSION()
        result = {'valids': [], 'invalids': []}
        query = session.query(Department.department, Job.job,
                        func.sum(case((extract('quarter', HiredEmployees.datetime) == 1, 1), else_=0)).label('q1'),
                        func.sum(case((extract('quarter', HiredEmployees.datetime) == 2, 1), else_=0)).label('q2'),
                        func.sum(case((extract('quarter', HiredEmployees.datetime) == 3, 1), else_=0)).label('q3'),
                        func.sum(case((extract('quarter', HiredEmployees.datetime) == 4, 1), else_=0)).label('q4')) \
        .join(Department, HiredEmployees.department_id == Department.id).join(Job,HiredEmployees.job_id == Job.id ) \
        .filter(extract('year', HiredEmployees.datetime) == year) \
        .group_by(Department.department, Job.job)

        records = query.all()

        result['valids'] = [{
            'department': record[0],
            'job': record[1],
            'Q1': record[2],
            'Q2': record[3],
            'Q3': record[4],
            'Q4': record[5],
        } for record in records]
        return result

    @staticmethod
    async def get_departments_above_average(year: int = 2021):
        session = SESSION()
        result = {'valids': [], 'invalids': []}
        total_employees = session.query(func.count(HiredEmployees.id)) \
            .filter(extract('year', HiredEmployees.datetime) == year) \
            .scalar()
        total_departments = session.query(func.count(Department.id)).scalar()
        mean = round(total_employees/total_departments)

        employee_counts = session.query(
            Department.department,
            Department.id,
            func.count(HiredEmployees.id).label('employee_count')
        ).join(HiredEmployees, Department.id == HiredEmployees.department_id) \
            .group_by(Department.department, Department.id) \
            .all()

        result['valids'] = [{
            'id': record[1],
            'department': record[0],
            'hired': record[2],
        } for record in employee_counts if record[2] > mean]

        return result
