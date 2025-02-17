import csv
from sqlalchemy import insert
from sqlalchemy import Column, Integer, String
from src.connectors.db_connect import ENGINE, BASE, SESSION, excecute


class Job(BASE):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    job = Column(String, unique=True)

    @staticmethod
    def __delete_schema__():
        '''Delete table'''
        BASE.metadata.tables['jobs'].drop(ENGINE)

    @staticmethod
    def __create_all_schemas__():
        '''Create table'''
        BASE.metadata.create_all(ENGINE)

    @staticmethod
    async def insert_jobs(jobs: list):
        result = {'valids':[], 'invalids':[]}
        to_insert = []
        obj = {}
        for element in jobs:
            if element.id:
                obj['id'] = element.id
            obj['job'] = element.job
            try:
                stmt = insert(Job).values(**obj).returning(Job)
                query_result = excecute(stmt).fetchone()
                to_insert.append({
                    'id':int(query_result[0]),
                    'job':str(query_result[1])
                    }
                )
            except Exception as e:
                result['invalids'].append(
                    {'id':element.id, 'job':element.job}
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
                    stmt = insert(Job).values(
                        id=int(element[0]),
                        job=str(element[1])
                        ).returning(Job)
                    query_result = excecute(stmt).fetchall()
                    if len(query_result) > 0:
                        to_insert.append({
                            'id':int(query_result[0][0]),
                            'job':str(query_result[0][1])
                            }
                        )
                except Exception as e:
                    result['invalids'].append(
                        {'id':element[0], 'job':element[1]}
                    )
                print(element)
        result['valids'] = to_insert
        return result