# import pytest
#
# from lynse.api.http_api.http_api import app
# from lynse.api.http_api.client_api import pack_data
#
#
# @pytest.fixture()
# def test_client():
#     app.config.update({
#         "TESTING": True,
#     })
#
#     yield app.test_client()
#
#
# def test_create_database(test_client):
#     url = 'http://localhost:7637/create_database'
#     data = {
#         "database_name": "example_database",
#         "drop_if_exists": True
#     }
#     response = test_client.post(url, json=data)
#     assert response.status_code == 200
#     assert response.json == {"status": "success", "params": {"database_name": "example_database"}}
#
#
# def create_collection(test_client):
#     url = 'http://localhost:7637/required_collection'
#     data = {
#         "database_name": "example_database",
#         "collection_name": "example_collection",
#         "dim": 4,
#         "chunk_size": 1024,
#         "distance": "L2",
#         "dtypes": "float32",
#         "use_cache": True,
#         "scaler_bits": 8,
#         "n_threads": 4,
#         "warm_up": True,
#         "drop_if_exists": True
#     }
#     response = test_client.post(url, json=data)
#
#
# def test_require_collection(test_client):
#     url = 'http://localhost:7637/required_collection'
#     data = {
#         "database_name": "example_database",
#         "collection_name": "example_collection",
#         "dim": 4,
#         "chunk_size": 1024,
#         "distance": "L2",
#         "dtypes": "float32",
#         "use_cache": True,
#         "scaler_bits": 8,
#         "n_threads": 4,
#         "warm_up": True,
#         "drop_if_exists": True
#     }
#     response = test_client.post(url, json=data)
#     print(response.json)
#     assert response.status_code == 200
#     assert response.json == {
#         "status": "success", "params":
#             {
#                 "database_name": "example_database",
#                 "collection_name": "example_collection",
#                 "dim": 4, "chunk_size": 1024, "distance": "L2",
#                 "dtypes": "float32", "use_cache": True, "scaler_bits": 8,
#                 "n_threads": 4, "warm_up": True, "drop_if_exists": True, "buffer_size": 20
#             }
#     }
#
#
# def test_add_item(test_client):
#     create_collection(test_client)  # create collection, drop_if_exists=True
#     url = 'http://localhost:7637/add_item'
#
#     vector = [0.1, 0.2, 0.3, 0.4]
#     data = {
#         "database_name": "example_database",
#         "collection_name": "example_collection",
#         "item": {
#             "vector": vector,
#             "id": 1,
#             "field": {
#                 "name": "example",
#                 "age": 18
#             },
#         },
#         "normalize": True
#     }
#
#     header = {
#         "Content-Type": "application/msgpack"
#     }
#
#     response = test_client.post(url, data=pack_data(data), headers=header)
#     print(response.json)
#     assert response.status_code == 200
#     assert response.json == {"status": "success", "params":
#         {
#             "database_name": "example_database",
#             "collection_name": "example_collection", "item":
#             {"id": 1}
#         }}
#
#     url = 'http://localhost:7637/commit'
#     data = {
#         "collection_name": "example_collection"
#     }
#     response = test_client.post(url, json=data)
#     assert response.status_code == 202
#
#     # test shape
#
#     url = 'http://localhost:7637/collection_shape'
#     data = {
#         "database_name": "example_database",
#         "collection_name": "example_collection"
#     }
#
#     response = test_client.post(url, json=data)
#     assert response.status_code == 200
#     assert response.json == {"status": "success",
#                              "params": {"database_name": "example_database",
#                                         "collection_name": "example_collection", "shape": [1, 4]}}
#
#
# def test_bulk_add_items(test_client):
#     create_collection(test_client)  # create collection, drop_if_exists=True
#     url = 'http://localhost:7637/bulk_add_items'
#     v0 = [0.1, 0.2, 0.3, 0.4]
#     v1 = [0.1, 0.2, 0.3, 0.4]
#     v2 = [0.2, 0.3, 0.4, 0.5]
#
#     data = {
#         "database_name": "example_database",
#         "collection_name": "example_collection",
#         "items": [
#             {
#                 "vector": v0,
#                 "id": 1,
#                 "field": {
#                     "name": "example",
#                     "age": 18
#                 }
#             },
#             {
#                 "vector": v1,
#                 "id": 2,
#                 "field": {
#                     "name": "example2",
#                     "age": 18
#                 },
#             },
#             {
#                 "vector": v2,
#                 "id": 3,
#                 "field": {
#                     "name": "example3",
#                     "age": 19
#                 },
#             }
#         ],
#         "normalize": True
#     }
#     response = test_client.post(url, json=data)
#
#     assert response.status_code == 200
#     assert response.json == {
#         "status": "success", "params":
#             {
#                 "database_name": "example_database",
#                 "collection_name": "example_collection",
#                 "ids": [1, 2, 3]
#             }
#     }
#
#     url = 'http://localhost:7637/commit'
#     data = {
#         "database_name": "example_database",
#         "collection_name": "example_collection"
#     }
#     response = test_client.post(url, json=data)
#     assert response.status_code == 202
#
#     url = 'http://localhost:7637/collection_shape'
#     data = {
#         "database_name": "example_database",
#         "collection_name": "example_collection"
#     }
#     response = test_client.post(url, json=data)
#     assert response.status_code == 200
#     assert response.json == {"status": "success",
#                              "params": {"database_name": "example_database",
#                                         "collection_name": "example_collection", "shape": [2, 4]}}
#
# def test_query(test_client):
#     url = 'http://localhost:7637/query'
#
#     data = {
#         "database_name": "example_database",
#         "collection_name": "example_collection",
#         "vector": [0.1, 0.2, 0.3, 0.4],
#         "k": 10,
#         'distance': 'cosine',
#         "query_filter": {
#             "must_fields": [
#                 {
#                     "key": "name",
#                     "matcher": {
#                         "value": "example",
#                         "comparator": "eq"
#                     }
#                 }
#             ],
#             "any_fields": [
#                 {
#                     "key": "age",
#                     "matcher": {
#                         "value": 18,
#                         "comparator": "eq"
#                     }
#                 }
#             ]
#         }
#     }
#
#     response = test_client.post(url, json=data)
#     assert response.status_code == 200
#
#     rjson = response.json
#     rjson['params']['items']['query time'] = 0.0
#     rjson['params']['items']['scores'] = [1]
#
#     assert rjson == {"status": "success", "params":
#         {"database_name": "example_database", "collection_name": "example_collection", "items": {
#             "k": 10, "ids": [1], "scores": [1],
#             "distance": 'cosine', "query time": 0.0
#         }}}
#
#
# def test_drop_collection(test_client):
#     url = 'http://localhost:7637/drop_collection'
#     data = {
#         "database_name": "example_database",
#         "collection_name": "example_collection"
#     }
#     response = test_client.post(url, json=data)
#     assert response.status_code == 200
#     assert response.json == {"status": "success",
#                              "params": {"database_name": "example_database", "collection_name": "example_collection"}}
#
#
# def test_show_collections(test_client):
#     url = 'http://localhost:7637/show_collections'
#     data = {
#         "database_name": "example_database"
#     }
#     response = test_client.post(url, json=data)
#     assert response.status_code == 200
#     assert response.json == {"status": "success", "params": {"collections": []}}
#
#
# def test_drop_database(test_client):
#     url = 'http://localhost:7637/drop_database'
#     data = {
#         "database_name": "example_database"
#     }
#     response = test_client.post(url, json=data)
#     assert response.status_code == 200
#     assert response.json == {"status": "success", "params": {"database_name": "example_database"}}
#
#
# def test_database_exists(test_client):
#     url = 'http://localhost:7637/database_exists'
#     data = {
#         "database_name": "example_database"
#     }
#     response = test_client.post(url, json=data)
#     assert response.status_code == 200
#     assert response.json == {"status": "success", "params": {"exists": False}}
