import json
import uuid
import asyncio
import base64
from typing import Optional
from src.connectors.db_connect import BASE
from datetime import datetime, timedelta, timezone
from src.connectors.long_process.base import BaseCRUD
from src.settings import JOB_MAX_ATTEMPTS, JOB_TIMEOUT_SEC
from sqlalchemy import JSON, BigInteger, Column, DateTime, LargeBinary, String, and_, select, text

class AsyncProcess(BASE, BaseCRUD):
    __tablename__ = 'mge_async_process'
    __failed__ = 'failed'
    __successful__ = 'successful'
    __notified__ = 'notified'
    __pending__ = 'pending'
    __in_progress__ = 'in_progress'
    __JOB_MAX_ATTEMPTS__ = JOB_MAX_ATTEMPTS
    __JOB_TIMEOUT__ = JOB_TIMEOUT_SEC

    id = Column(LargeBinary(500), primary_key=True, nullable=False)
    event_type = Column( String(500), nullable=False)
    status = Column(String(500), nullable=False)
    input = Column(JSON, nullable=False)
    output = Column(JSON)
    job_metadata = Column(JSON)
    attempts = Column(BigInteger)
    created_by = Column(String(500))
    created_timestamp_utc = Column(DateTime, nullable=False)
    updated_by = Column(String(500))
    updated_timestamp_utc = Column(DateTime, nullable=False)


    @classmethod
    @BaseCRUD.with_session
    def get_recent_scenarios(cls, created_by: Optional[str], time_interval: int=30, **kwargs) -> list:
        """
        Retrieve all recently created scenarios for a given user and time interval.

        :param created_by: The user ID that created the scenarios.
        :type created_by: str
        :param time_interval: The number of minutes to go back in time to retrieve scenarios.
        :type time_interval: int
        :return: A list of dictionaries containing the scenarios in the last time interval.
        :rtype: list
        """
        session = kwargs['session']
        thirty_mins_ago = datetime.utcnow() - timedelta(minutes=time_interval)
        conditions = [
            AsyncProcess.created_timestamp_utc >= thirty_mins_ago
        ]
        if created_by is not None:
            conditions.append(AsyncProcess.created_by == created_by)
        query = select(cls).where(and_(*conditions))
        results = session.execute(query).fetchall()
        return [AsyncProcess(**(x[0].to_dict())) for x in results]

    @classmethod
    @BaseCRUD.with_session
    def insert_message(cls, event_type, status, input, attempts, created_by, updated_by, **kwargs) -> dict:
        """
        Inserts a new message into the database.

        Parameters:
        ----------
        event_type: str
            The type of event this message belongs to.
        status: str
            The status of the message.
        input: dict
            The input data for the message.
        attempts: int
            The number of attempts made to process this message.
        created_by: str
            The user who created the message.
        updated_by: str
            The user who last updated the message.
        **kwargs: dict
            Additional keyword arguments.

        Returns:
        -------
        dict
            The newly inserted record as a dictionary.
        """
        session = kwargs['session']
        new_record = AsyncProcess(
            id=base64.b64encode(str(uuid.uuid4()).encode()),
            event_type=event_type,
            status=status,
            input=input,
            attempts=attempts,
            created_by=created_by,
            updated_by=updated_by,
            created_timestamp_utc = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
            updated_timestamp_utc = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
        )
        session.add(new_record)

        return new_record.to_dict()

    @classmethod
    @BaseCRUD.with_session
    async def event_stream(cls, **kwargs):
        """
        Event stream for the results of long-running processes.

        This generator yields new events as they are available. If no new events are available, it sends a heartbeat message.

        The event stream is filtered by process status: only processes with a status of 'successful' are considered.

        The stream will be closed after the first iteration.

        :param kwargs: Additional keyword arguments passed to the BaseCRUD.with_session decorator.
        :return: An async generator of messages.
        """
        while True:
            records = cls.custom_filter(where_dict={'status': cls.__successful__}, columns=['id', 'created_by', 'output'])
            if records:
                for record in records:
                    response = {
                        'id': record['id'].decode(),
                        'user': record['created_by'],
                        'response': record['output']['response'],
                    }
                    yield f'data: {json.dumps(response)}\n\n'
                    cls.update_by_filter(
                        filter_criteria={'id': record['id']},
                        update_values={'status': cls.__notified__}
                        )
            yield ": heartbeat\n\n"
            await asyncio.sleep(3)
