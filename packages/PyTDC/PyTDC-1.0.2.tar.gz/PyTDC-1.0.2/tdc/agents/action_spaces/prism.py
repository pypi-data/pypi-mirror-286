from .datasets import base as data_base
from .datasets import datasets
from .resource import base as resource_base
from .resource import resources
from .resource import resource_entities

import json

class PrismTxT(dict):
    
    def __init__(self):
        self["entity_classes"] = {
            "Dataset": data_base,
            "Resource": resource_base,
        }
        self["entities"] = {
            "Dataset": [x.get_json() for x in datasets],
            "Resource": [x.get_json() for x in resource_entities]
        }
        # add properties as dictionary entries to the entity base classes
        for _, e in self["entity_classes"].items():
            e["instructions"] = e.entity_class_instructions,
            e["description"] = e.entity_class_description,
            e["functions"] = e.entity_class_functions
        
        for k in self["entity_classes"]:
            self["entity_classes"][k] = self["entity_classes"][k].get_json()

        self["description"] = "parent class for Prism instruction tuning. can be used to load any prism TDC dataset. see instructions for examples."
        self["instructions"] = "Let P be instance of PrismTxt. Then get_dataset is specified as f(name) -> dataset. Example usage here: \
            P.get_dataset('BindingDB_IC50') -> DataFrame ; P.get_dataset('GDSC1') -> DataFrame\n\n In order to use the TDC resource, see individual JSONS for each\
                of {}".format(resources)
            
    def get_json(self):
        return json.dumps(self, indent=4)
    
    def get_dataset(self, ds):
        for x in datasets:
            if x["name"] == ds:
                return x.get()
        all_ds = [x["name"] for x in datasets]
        raise Exception("dataset {} not in datasets list {}".format(ds, all_ds))