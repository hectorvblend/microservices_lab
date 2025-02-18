#!/usr/bin/env python

"""
The purpose of this module is to store all the `base-models` of the parameters
used in the APIs for validation, likewise, it contains tools for managing them.
For more info of how to build `base-models`, see: https://pydantic-docs.helpmanual.io/usage/models/
"""
from pydantic import BaseModel

#----------------------------------Messages---------------------------------

class SendMessage(BaseModel):
    message: str
    user: str
