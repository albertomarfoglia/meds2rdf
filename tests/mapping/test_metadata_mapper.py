from rdflib import Graph, Literal, XSD
from meds2rdf.mapping.metadata_mapper import map_dataset_metadata
from meds2rdf.namespace import MEDS

def test_map_dataset_metadata_adds_triples():
    graph = Graph()
    
    metadata = {
        "dataset_name": "Demo Dataset",
        "meds_version": "0.3.3",
        "created_at": "2025-01-01T00:00:00"
    }
    
    dataset_uri = map_dataset_metadata(graph, metadata)

    assert(dataset_uri, None, MEDS.DatasetMetadata) in graph
    assert (dataset_uri, MEDS.datasetName, Literal("Demo Dataset", datatype=XSD.string)) in graph
    assert (dataset_uri, MEDS.medsVersion, Literal("0.3.3", datatype=XSD.string)) in graph
    assert (dataset_uri, MEDS.createdAt, Literal("2025-01-01T00:00:00", datatype=XSD.dateTime)) in graph
