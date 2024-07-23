"""
Base class for the action space. An entity.
"""

import json

class Entity(dict):
    
    _UNSERIALIZABLE = [
        "lambda_f"
    ]
    def __init__(self, **kwargs):
        super(Entity, self).__init__(**kwargs)
        self._description = None
        self._functions = None
        self._main = None
        self._instructions = None
        
    def get_json(self):
        o = dict(**self)
        # remove unserializable keys
        for u in self._UNSERIALIZABLE:
            if u in o:
                del o[u]
        return json.dumps(o, indent=4)

    @property
    def entity_class_description(self):
        assert self._description is not None, "Entity description is None for {}".format(type(self))
        return json.dumps(self._description, indent=4)
    
    @property
    def entity_class_functions(self):
        assert self._functions is not None, "Entity functions is None for {}".format(type(self))
        return json.dumps(self._functions, indent=4)
    
    @property
    def entity_class_main(self):
        assert self._main is not None, "Entity main is None for {}".format(type(self))
        return self._main
    
    @property
    def entity_class_instructions(self):
        assert self._instructions is not None, "Entity instructions is None for {}".format(type(self))
        return self._instructions