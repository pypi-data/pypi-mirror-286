# Auto generated from jsonLDObject.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-07-22T08:19:54
# Schema: jsonld
#
# id: https://w3id.org/cde/jsonld/v1.0/
# description: jsonld base class
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from datetime import date, datetime
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
CRED = CurieNamespace('cred', 'https://w3id.org/vc/')
DC = CurieNamespace('dc', 'http://purl.org/dc/elements/1.1/')
JSONLD = CurieNamespace('jsonld', 'https://w3id.org/cde/jsonld/v1.0/#')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RDF = CurieNamespace('rdf', 'https://www.w3.org/RDF/')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
VS = CurieNamespace('vs', 'http://www.w3.org/2003/06/sw-vocab-status/ns#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = JSONLD


# Types

# Class references
class JsonLDObjectId(extended_str):
    pass


@dataclass
class JsonLDObject(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = JSONLD["JsonLDObject"]
    class_class_curie: ClassVar[str] = "jsonld:JsonLDObject"
    class_name: ClassVar[str] = "JsonLDObject"
    class_model_uri: ClassVar[URIRef] = JSONLD.JsonLDObject

    id: Union[str, JsonLDObjectId] = None
    hasLabel: Optional[Union[str, List[str]]] = empty_list()
    hasDescription: Optional[Union[str, List[str]]] = empty_list()
    hasComment: Optional[Union[str, List[str]]] = empty_list()
    hasTitle: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, JsonLDObjectId):
            self.id = JsonLDObjectId(self.id)

        if not isinstance(self.hasLabel, list):
            self.hasLabel = [self.hasLabel] if self.hasLabel is not None else []
        self.hasLabel = [v if isinstance(v, str) else str(v) for v in self.hasLabel]

        if not isinstance(self.hasDescription, list):
            self.hasDescription = [self.hasDescription] if self.hasDescription is not None else []
        self.hasDescription = [v if isinstance(v, str) else str(v) for v in self.hasDescription]

        if not isinstance(self.hasComment, list):
            self.hasComment = [self.hasComment] if self.hasComment is not None else []
        self.hasComment = [v if isinstance(v, str) else str(v) for v in self.hasComment]

        if not isinstance(self.hasTitle, list):
            self.hasTitle = [self.hasTitle] if self.hasTitle is not None else []
        self.hasTitle = [v if isinstance(v, str) else str(v) for v in self.hasTitle]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=JSONLD.id, name="id", curie=JSONLD.curie('id'),
                   model_uri=JSONLD.id, domain=None, range=URIRef)

slots.hasLabel = Slot(uri=RDFS.label, name="hasLabel", curie=RDFS.curie('label'),
                   model_uri=JSONLD.hasLabel, domain=None, range=Optional[Union[str, List[str]]])

slots.hasComment = Slot(uri=RDFS.comment, name="hasComment", curie=RDFS.curie('comment'),
                   model_uri=JSONLD.hasComment, domain=None, range=Optional[Union[str, List[str]]])

slots.hasTitle = Slot(uri=DC.title, name="hasTitle", curie=DC.curie('title'),
                   model_uri=JSONLD.hasTitle, domain=None, range=Optional[Union[str, List[str]]])

slots.hasDescription = Slot(uri=DC.description, name="hasDescription", curie=DC.curie('description'),
                   model_uri=JSONLD.hasDescription, domain=None, range=Optional[Union[str, List[str]]])
