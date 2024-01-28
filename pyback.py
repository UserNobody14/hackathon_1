from llama_index.embeddings import HuggingFaceEmbedding
from milvus import default_server
from pymilvus import (
    utility,
    connections,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
)

embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L12-v2")


# vector_store = MilvusVectorStore(
#     collection_name="palmyra_small_test",
#     host="127.0.0.1",
#     port=default_server.listen_port,
#     dim=384,
#     schema=schema
# )


####################
# insert data
def insert_data(dd):
    collection = Collection("confusing_sign")
    print(collection.schema)
    ccc = []
    for eachdata in dd:
        # transform into confusing sign item
        embdf = embed_model.get_text_embedding(
            eachdata["text"]
        )  # Get an existing collection.
        # print(embdf)
        collection.insert(
            [
                {
                    "confusing_sign_text": eachdata["text"],
                    "confusing_sign_text_embedding": embdf,
                    "confusing_sign_json": eachdata["json"],
                }
            ]
        )
    # Insert data.
    # collection.insert(ccc)


####################


#####################


def run_search(query):
    # with default_server:
    #     default_server.set_base_dir('milvus_data')
    collection = Collection("confusing_sign")  # Get an existing collection.
    collection.load()

    embdf = embed_model.get_text_embedding(query)  # Get query.

    search_params = {
        "metric_type": "L2",
        "offset": 0,
        "ignore_growing": False,
        "params": {"nprobe": 10},
    }

    results = collection.search(
        data=[embdf],
        anns_field="confusing_sign_text_embedding",
        # the sum of `offset` in `param` and `limit`
        # should be less than 16384.
        param=search_params,
        limit=1,
        expr=None,
        # set the names of the fields you want to
        # retrieve from the search result.
        output_fields=["confusing_sign_json"],
        consistency_level="Strong",
    )

    # get the IDs of all returned hits
    results[0].ids

    # get the distances to the query vector from all returned hits
    results[0].distances

    print("////////////////")
    print(results)
    print("////////////////")
    # get the value of an output field specified in the search request.
    hit = results[0][0]
    rres = hit.entity.get("confusing_sign_json")
    print(rres)
    return rres


#####################


def setup_unitial():
    # default_server.start()
    # utility.drop_collection("confusing_sign")

    # create a milvus table with the name of the confusing sign, a json for the confusing sign
    # and a vector for the confusing sign
    connections.connect(
        host="127.0.0.1",
        port=default_server.listen_port,
    )
    if utility.has_collection("confusing_sign"):
        utility.drop_collection("confusing_sign")
    if not utility.has_collection("confusing_sign"):
        confusing_sign_id = FieldSchema(
            name="confusing_sign_id",
            dtype=DataType.INT64,
            is_primary=True,
            auto_id=True,
        )
        confusing_sign_json = FieldSchema(
            name="confusing_sign_json", max_length=512, dtype=DataType.VARCHAR
        )
        confusing_sign_text = FieldSchema(
            name="confusing_sign_text", max_length=512, dtype=DataType.VARCHAR
        )
        confusing_sign_text = FieldSchema(
            name="confusing_sign_text_embedding", dtype=DataType.FLOAT_VECTOR, dim=384
        )
        schema = CollectionSchema(
            fields=[
                confusing_sign_id,
                confusing_sign_json,
                confusing_sign_text,
            ],
            enable_dynamic_field=True,
        )
        collection = Collection("confusing_sign", schema)
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 1536},
        }
        collection.create_index(
            field_name="confusing_sign_text_embedding", index_params=index_params
        )
    else:
        collection = Collection("confusing_sign")
    collection.load()
    print(collection.schema)
    try:
        insert_data(
            [
                {
                    "text": "This is a confusing sign",
                    "json": r"""{
                "canpark": "false"
                }""",
                },
                {
                    "text": "You can park here",
                    "json": r"""{
                "canpark": "true"
                }""",
                },
                {
                    "text": "No parking here",
                    "json": r"""{
                "canpark": "false"
                }""",
                },
                {
                    "text": "Parking allowed here",
                    "json": r"""{
                "canpark": "true"
                }""",
                },
            ]
        )
    except:  # noqa: E722
        pass


setup_unitial()
