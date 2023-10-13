# Planned feature.
# from pydantic import Extra
# class Lookup(BaseModel):
#     class Config:
#         extra = Extra.allow # or 'allow' str
#     lookup: str

    # def to_sql(self) -> str:
    #     m = self.model_dump()
    #     query = f"SELECT {m['lookup']} FROM {m['type']} WHERE"
    #     # map type to a type object, then map all keys passed to the actual names in the database.
    #     del m["lookup"]
    #     del m["type"]

    #     for k, v in m.items():
    #         query += f" `{k}`=`{v}`"
    #     return query


Lookup = int # Replace me with the lookup class
LookupID = (Lookup | int)
