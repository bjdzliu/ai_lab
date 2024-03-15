'''

docker run -d -p 8000:3000 -e HOST_URL=http://{host_ip}:8000 -e MILVUS_URL=127.0.0.1:19530 zilliz/attu:latest

jina-embeddings-v2-small-en: 33 million parameters, 512-dimension embeddings.
jina-embeddings-v2-base-en: 137 million parameters, 768-dimension embeddings.
jina-embeddings-v2-large-en: 435 million parameters, 1,024-dimension embeddings.

http://xxxxxx:8000/#/collections

'''


from pymilvus import(
    connections,
    db,
    utility,
    FieldSchema,
    Collection,
    DataType,
    CollectionSchema

)

import os

os.environ['HF_TOKEN'] = "xxxxxx"

print(os.getenv('HF_TOKEN'))

# connect to a server
connections.connect("default",host='xxxxxxx',port='19530')
print(db.list_database())
print(utility.list_collections())


def create_demo():
    #Creating a Collection in Milvus
    fields=[
        FieldSchema(name="pk",dtype=DataType.INT64,is_primary=True,auto_id=False),
        FieldSchema(name="words",dtype=DataType.VARCHAR,max_length=50),
        FieldSchema(name="embeddings",dtype=DataType.FLOAT_VECTOR,dim=512),
    ]
    # similier with teh table in relation db
    schema=CollectionSchema(fields,"simple demo for storing and receive from Google")


    demo=Collection('demo_test',schema)

    # 
    # from langchain.embeddings import HuggingFaceEmbeddings
    # from langchain.vectorstores import Chroma
    # model_name="jinaai/jina-embeddings-v2-small-en"

    from transformers import AutoModel
    from numpy.linalg import norm
    model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-small-en', trust_remote_code=True) 

    embeddings = model.encode(['dog','puppy','queen','book','lion'])

    data=[
    [1,2,3,4,5],
    ['dog','puppy','queen','book','lion',],
    embeddings
    ]

    insert_result=demo.insert(data)

    ## because the data is small, so choose  FLAT
    ## L2: 欧式距离
    index={
        
        "index_type":"FLAT",
        "metric_type":"L2",
        "params":{}
    }
    demo.create_index("embeddings",index)

    demo.load()

def delete_collection():
    from pymilvus import utility
    utility.drop_collection("demo_test")


# def test():
#     data=[dog]


if __name__ == "__main__":
    delete_collection()
    create_demo()
