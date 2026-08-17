from pydantic import BaseModel, Field
class ChecklistCreate(BaseModel):
 title:str|None=Field(default=None,max_length=180); base_key:str|None=Field(default=None,max_length=80)
class ChecklistUpdate(BaseModel): checked:bool
class ChecklistRead(BaseModel): id:int; base_key:str|None; title:str|None; checked:bool
