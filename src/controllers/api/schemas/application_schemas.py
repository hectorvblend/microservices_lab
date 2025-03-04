#!/usr/bin/env python

"""
The purpose of this module is to store all the `base-models` of the parameters
used in the APIs for validation, likewise, it contains tools for managing them.
For more info of how to build `base-models`, see: https://pydantic-docs.helpmanual.io/usage/models/
"""
from pydantic import BaseModel
from typing import Optional, Union, List

#----------------------------------Jobs---------------------------------

class JobStructure(BaseModel):
    id: Optional[Union[int, None]]
    job: str

class InsertJob(BaseModel):
    """
    Params to insert a new Job to the list.
    """
    jobs : List[JobStructure]

#----------------------------------Department---------------------------------

class DepartmentStructure(BaseModel):
    id: Optional[Union[int, None]]
    department: str

class InsertDepartment(BaseModel):
    """
    Params to insert a new Department to the list.
    """
    departments : List[DepartmentStructure]


#----------------------------------HiredEmployees---------------------------------

class HiredEmployeesStructure(BaseModel):
    id: Optional[Union[int, None]]
    name: str
    department_id: Optional[Union[int, None]]
    job_id: Optional[Union[int, None]]

class InsertHiredEmployees(BaseModel):
    """
    Params to insert a new Department to the list.
    """
    hired_employees : List[HiredEmployeesStructure]