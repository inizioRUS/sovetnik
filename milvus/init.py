from pymilvus import CollectionSchema, FieldSchema, DataType, MilvusClient

client = MilvusClient(uri="http://localhost:19530")

if client.has_collection(collection_name="sibintek"):
    client.drop_collection(collection_name="sibintek")

id_ask = FieldSchema(
    name="id",
    dtype=DataType.INT64,
    is_primary=True,
)
type_s = FieldSchema(
    name="type",
    dtype=DataType.VARCHAR,
    max_length=65535,
)

ask_intro = FieldSchema(
    name="ask_vector",
    dtype=DataType.FLOAT_VECTOR,
    dim=1024,
)
ask_solve = FieldSchema(
    name="ask_solve",
    dtype=DataType.VARCHAR,
    max_length=65535,
)
schema = CollectionSchema(
    fields=[id_ask, type_s, ask_intro, ask_solve],
    description="AsK SIBINTEK"
)
collection_name = "sibintek"


client.create_collection(collection_name=collection_name, schema=schema)

index_params = MilvusClient.prepare_index_params()

index_params.add_index(
    field_name="ask_vector",
    metric_type="COSINE",
    index_type="IVF_FLAT",
    index_name="vector_index",
    params={"nlist": 1024}
)


client.create_index(
    collection_name="sibintek",
    index_params=index_params,
    sync=False
)

if client.has_collection(collection_name="sibintek_guide"):
    client.drop_collection(collection_name="sibintek_guide")

id_ask = FieldSchema(
    name="id",
    dtype=DataType.INT64,
    is_primary=True,
)
filename = FieldSchema(
    name="filename",
    dtype=DataType.VARCHAR,
    max_length=65535,
)

guide_vector = FieldSchema(
    name="guide_vector",
    dtype=DataType.FLOAT_VECTOR,
    dim=1024,
)

schema = CollectionSchema(
    fields=[id_ask, filename, guide_vector],
    description="AsK SIBINTEK"
)
collection_name = "sibintek_guide"


client.create_collection(collection_name=collection_name, schema=schema)

index_params = MilvusClient.prepare_index_params()

index_params.add_index(
    field_name="guide_vector",
    metric_type="COSINE",
    index_type="IVF_FLAT",
    index_name="guide_vector_index",
    params={"nlist": 1024}
)


client.create_index(
    collection_name="sibintek_guide",
    index_params=index_params,
    sync=False
)