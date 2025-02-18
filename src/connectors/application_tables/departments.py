import csv
from sqlalchemy import insert
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from src.connectors.db_connect import ENGINE, BASE, excecute


class Department(BASE):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    department = Column(String, unique=True)

    @staticmethod
    def __delete_schema__():
        '''Delete table'''
        BASE.metadata.tables['departments'].drop(ENGINE)

    @staticmethod
    def __create_all_schemas__():
        '''Create table'''
        BASE.metadata.create_all(ENGINE)

    @staticmethod
    async def insert_departments(departments: list):
        result = {'valids':[], 'invalids':[]}
        to_insert = []
        obj = {}
        for element in departments:
            if element.id:
                obj['id'] = element.id
            obj['department'] = element.department
            try:
                stmt = insert(Department).values(**obj).returning(Department)
                query_result = excecute(stmt).fetchone()
                to_insert.append({
                    'id':int(query_result[0]),
                    'department':str(query_result[1])
                    }
                )
            except Exception as e:
                result['invalids'].append(
                    {'id':element.id, 'department':element.department}
                )
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
                try:
                    stmt = insert(Department).values(
                        id=int(element[0]),
                        department=str(element[1])
                        ).returning(Department)
                    query_result = excecute(stmt).fetchall()
                    if len(query_result) > 0:
                        to_insert.append({
                            'id':int(query_result[0][0]),
                            'department':str(query_result[0][1])
                            }
                        )
                except Exception as e:
                    result['invalids'].append(
                        {'id':element[0], 'department':element[1]}
                    )
                print(element)
        result['valids'] = to_insert
        return result