"""
Tools for using marshmallow/toastedmarshmallow for json->obj->json marshalling stuff.
"""

from marshmallow import Schema, fields, post_load, ValidationError


class JsonSerializable:
    """
    Simple type wrapper mixin for json serialize/deserialize of objects to reduce boilerplate.

    To use: add as a parent type and set __schema__ at the class level to the JitSchema-subclassed object that is the json schema to use.
    Then call <class>.from_json(dict) and <obj>.to_json()

    Example:
        {'bucket': 'xx', 'key': 'blah'} -> obj
        obj = ObjectStoreLocation.from_json(json.loads(input_string))
        obj.to_json() # Gives a dict
        obj.to_json_str() # Gives a string serialized json output

        class ObjectStoreLocation(JsonMappedMixin):
          class ObjectStoreLocationV1Schema(JitSchema):
            bucket = fields.Str()
            key = fields.Str()

            # This tells the system to return the actual object type rather than a serialization result
            @post_load
            def make(self, data):
              return ObjectStoreLocation(**data)


          # Set the schema ref. This doesn't strictly have to be a child-class, could be outside the parent type. Done here for clarity
          __schema__ = ObjectStoreLocationV1Schema()

          # Needs a kwargs-style constructor for the @post_load/make() call to work
          def __init__(self, bucket=None, key=None):
            self.bucket = bucket
            self.key = key


    """

    __schema__: Schema = None

    @classmethod
    def from_json(cls, data):
        return cls.__schema__.load(data)

    def to_json(self):
        return self.__schema__.dump(self)

    def to_json_str(self):
        return self.__schema__.dumps(self)
