from rdflib import Graph, URIRef
from rdflib.namespace import XSD
from typing import Optional, Iterable
from ..meds2rdf.namespace import MEDS
from ..utils.rfd_utilis import *

def map_code(
    g: Graph,
    row: dict,
    dataset_uri: Optional[URIRef] = None
) -> URIRef:
    """
    Map a single row of a MEDS CodeSchema into a Code RDF individual.

    Parameters
    ----------
    g : Graph
        RDF graph to populate
    row : dict
        Dictionary representing a single code (code, descrption, parent_codes, etc.)
    dataset_uri : Optional[URIRef]
        URI of the dataset metadata to link via prov:wasDerivedFrom

    Returns
    -------
    URIRef
        URI of the created Code individual
    """

    code_str = try_access_mandatory_field_value(row=row, field="code", entity="Code")
    code_uri = add_code(code_str=code_str, graph=g, dataset_uri=dataset_uri)

    opt_lit_dict = {
        "description": (MEDS.codeDescription, XSD.string),
    }

    for column_name, (p, dtype) in opt_lit_dict.items():
        if_column_is_present(column_name, row, lambda v: g.add((code_uri, p, to_literal(v, dtype))))

    if_column_is_present("parent_codes", row, lambda v: g.add((code_uri, MEDS.parentCode, add_code(code_str=v, graph=g))))

    return code_uri


def map_code_table(
    g: Graph,
    data: Iterable[dict],
    dataset_uri: Optional[URIRef] = None
) -> list[URIRef]:
    """
    Map an iterable of MEDS CodeSchema rows to RDF Code individuals.

    Parameters
    ----------
    g : Graph
        RDF graph to populate
    data : Iterable[dict]
        List of rows/dicts representing the MEDS CodeSchema
    dataset_uri : Optional[URIRef]
        URI of the dataset metadata to link all codes to

    Returns
    -------
    list[URIRef]
        List of URIs of the created Code individuals
    """
    uris = []
    for row in data:
        code_uri = map_code(g, row, dataset_uri)
        uris.append(code_uri)
    return uris
