import json
import os
import shutil
import uuid
from threading import Thread

import msgpack

from flask import Flask, request, jsonify, Response
from waitress import serve
import socket

from lynse.configs.config import config
from lynse.core_components.kv_cache import IndexSchema
from lynse.core_components.limited_dict import LimitedDict
from lynse.core_components.safe_dict import SafeDict


app = Flask(__name__)

data_dict = LimitedDict(max_size=1000)

root_path = config.LYNSE_DEFAULT_ROOT_PATH
root_path_parent = root_path.parent


@app.before_request
def handle_msgpack_input():
    if request.headers.get('Content-Type') == 'application/msgpack':
        data = msgpack.unpackb(request.get_data(), raw=False)
        request.decoded_data = data


@app.route('/', methods=['GET'])
def index():
    return Response(json.dumps({'status': 'success', 'message': 'LynseDB HTTP API'}), mimetype='application/json')


@app.route('/required_collection', methods=['POST'])
def required_collection():
    """Create a collection in the database.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'chunk_size' not in data:
        data['chunk_size'] = 100000
    if 'distance' not in data:
        data['distance'] = 'cosine'
    if 'dtypes' not in data:
        data['dtypes'] = 'float32'
    if 'use_cache' not in data:
        data['use_cache'] = True
    if 'scaler_bits' not in data:
        data['scaler_bits'] = 8
    if 'n_threads' not in data:
        data['n_threads'] = 10
    if 'warm_up' not in data:
        data['warm_up'] = True
    if 'drop_if_exists' not in data:
        data['drop_if_exists'] = False
    if 'description' not in data:
        data['description'] = None
    if 'cache_chunks' not in data:
        data['cache_chunks'] = 20

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        my_vec_db.require_collection(
            collection=data['collection_name'],
            dim=data['dim'],
            chunk_size=data['chunk_size'],
            distance=data['distance'],
            dtypes=data['dtypes'],
            use_cache=data['use_cache'],
            scaler_bits=data['scaler_bits'],
            n_threads=data['n_threads'],
            warm_up=data['warm_up'],
            drop_if_exists=data['drop_if_exists'],
            description=data['description'],
            cache_chunks=data['cache_chunks']
        )

        return Response(json.dumps({
            'status': 'success',
            'params': {
                'database_name': data['database_name'],
                'collection_name': data['collection_name'],
                'dim': data['dim'], 'chunk_size': data['chunk_size'],
                'distance': data['distance'], 'dtypes': data['dtypes'],
                'use_cache': data['use_cache'], 'scaler_bits': data['scaler_bits'],
                'n_threads': data['n_threads'],
                'warm_up': data['warm_up'], 'drop_if_exists': data['drop_if_exists'],
                'cache_chunks': data['cache_chunks']
            }
        }, sort_keys=False), mimetype='application/json')

    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/drop_collection', methods=['POST'])
def drop_collection():
    """Drop a collection from the database.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        my_vec_db.drop_collection(data['collection_name'])

        return Response(json.dumps(
            {
                'status': 'success', 'params': {
                'database_name': data['database_name'],
                'collection_name': data['collection_name']
            }
            },
            sort_keys=False),
            mimetype='application/json')

    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/drop_database', methods=['POST'])
def drop_database():
    """Drop the database.

    Returns:
        dict: The status of the operation.
    """
    data = request.json
    try:
        shutil.rmtree(root_path / data['database_name'])

        return Response(json.dumps({
            'status': 'success'
        }, sort_keys=False),
            mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/database_exists', methods=['POST'])
def database_exists():
    """Check if the database exists.

    Returns:
        dict: The status of the operation.
    """
    data = request.json
    try:
        exists = (root_path / data['database_name']).exists()
        return Response(json.dumps({
            'status': 'success', 'params': {
                'exists': True if exists else False
            }
        },
            sort_keys=False), mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/show_collections', methods=['POST'])
def show_collections():
    """Show all collections in the database.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collections = my_vec_db.show_collections()
        return Response(json.dumps({
            'status': 'success', 'params': {
                'database_name': data['database_name'],
                'collections': collections
            }
        },
            sort_keys=False), mimetype='application/json')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/add_item', methods=['POST'])
def add_item():
    from lynse.api.native_api.high_level import LocalClient

    if request.headers.get('Content-Type') == 'application/msgpack':
        data = request.decoded_data
    else:
        data = request.json

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])
        id = collection.add_item(vector=data['item']['vector'], id=data['item']['id'],
                                 field=data['item'].get('field', {}), normalize=data['normalize'])

        return Response(json.dumps(
            {
                'status': 'success', 'params': {
                'database_name': data['database_name'],
                'collection_name': data['collection_name'], 'item': {
                    'id': data['item']['id']
                }
            }
            }, sort_keys=False),
            mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/bulk_add_items', methods=['POST'])
def bulk_add_items():
    from lynse.api.native_api.high_level import LocalClient

    if request.headers.get('Content-Type') == 'application/msgpack':
        data = request.decoded_data
    else:
        data = request.json

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])
        items = []
        for item in data['items']:
            items.append((item['vector'], item['id'], item.get('field', None)))
        ids = collection.bulk_add_items(items, normalize=data['normalize'])

        return Response(json.dumps({
            'status': 'success', 'params': {
                'database_name': data['database_name'],
                'collection_name': data['collection_name'], 'ids': [i['id'] for i in data['items']]
            }
        }, sort_keys=False),
            mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/search', methods=['POST'])
def search():
    """Search the database for the vectors most similar to the given vector.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient
    from lynse.core_components.kv_cache.filter import Filter

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'k' not in data:
        data['k'] = 10

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])

        if data['search_filter'] is None:
            search_filter = None
        else:
            search_filter = Filter().load_dict(data['search_filter'])

        ids, scores, field = collection.search(
            vector=data['vector'], k=data['k'],
            search_filter=search_filter,
            distance=data.get('distance', 'IP'),
            normalize=data.get('normalize', False),
            return_fields=data.get('return_fields', False)
        )

        if ids is not None:
            ids = ids.tolist()
            scores = scores.tolist()

        return Response(json.dumps(
            {
                'status': 'success', 'params': {
                    'database_name': data['database_name'],
                    'collection_name': data['collection_name'], 'items': {
                        'k': data['k'], 'ids': ids, 'scores': scores,
                        'fields': field,
                        'distance': collection.most_recent_search_report['Search Distance'],
                        'search time': collection.most_recent_search_report['Search Time']
                    }
                }
            }, sort_keys=False),
            mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


tasks = SafeDict()


def commit_task(data):
    from lynse.api.native_api.high_level import LocalClient

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])
        if 'items' in data:
            items = []
            for item in data['items']:
                items.append((item['vector'], item['id'], item.get('field', {})))

            collection.bulk_add_items(items)

        collection.commit()

        return {'status': 'Success', 'result': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name']
        }}
    except KeyError as e:
        return {'status': 'Error', 'message': f' missing required parameter {e}'}
    except Exception as e:
        return {'status': 'Error', 'message': str(e)}


@app.route('/commit', methods=['POST'])
def commit():
    if request.headers.get('Content-Type') == 'application/msgpack':
        data = request.decoded_data
    else:
        data = request.json

    if not data:
        return jsonify({'error': '未提供数据'}), 400

    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'Processing'}

    def execute_task():
        result = commit_task(data)
        tasks[task_id] = result

    thread = Thread(target=execute_task)
    thread.start()

    return jsonify({'task_id': task_id}), 202


@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': '任务未找到'}), 404

    return jsonify(task)


@app.route('/collection_shape', methods=['POST'])
def collection_shape():
    """Get the shape of a collection.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])
        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'], 'shape': collection.shape
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/set_environment', methods=['POST'])
def set_environment():
    """Set the environment variables.

    Returns:
        dict: The status of the operation.
    """
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        for key, value in data.items():
            os.environ[key] = value
        return Response(json.dumps({'status': 'success', 'params': data}, sort_keys=False), mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_environment', methods=['GET'])
def get_environment():
    """Get the environment variables.

    Returns:
        dict: The status of the operation.
    """
    env_list = ['LYNSE_LOG_LEVEL', 'LYNSE_LOG_PATH', 'LYNSE_TRUNCATE_LOG', 'LYNSE_LOG_WITH_TIME',
                'LYNSE_KMEANS_EPOCHS', 'LYNSE_SEARCH_CACHE_SIZE']

    params = {key: eval("global_config.key") for key in env_list}
    try:
        return Response(json.dumps({'status': 'success', 'params': params}, sort_keys=False),
                        mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_collection_search_report', methods=['POST'])
def get_collection_search_report():
    """Get the search report of a collection.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'], 'search_report': collection.search_report_
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_collection_status_report', methods=['POST'])
def get_collection_status_report():
    """Get the status report of a collection.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])

        db_report = {'DATABASE STATUS REPORT': {
            'Database shape': (
                0, collection._matrix_serializer.dim) if collection._matrix_serializer.IS_DELETED else collection.shape,
            'Database last_commit_time': collection._matrix_serializer.last_commit_time,
            'Database commit status': collection._matrix_serializer.COMMIT_FLAG,
            'Database distance': collection._distance,
            'Database use_cache': collection._use_cache,
            'Database status': 'DELETED' if collection._matrix_serializer.IS_DELETED else 'ACTIVE'
        }}

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'], 'status_report': db_report
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/is_collection_exists', methods=['POST'])
def is_collection_exists():
    """Check if a collection exists.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'],
            'exists': data['collection_name'] in my_vec_db.show_collections()
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_collection_config', methods=['POST'])
def get_collection_config():
    """Get the configuration of a collection.

    Returns:
        dict: The status of the operation.
    """
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        config_json_path = root_path / data['database_name'] / 'collections.json'
        with open(config_json_path, 'r') as file:
            collections = json.load(file)
            collection_config = collections[data['collection_name']]

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'], 'config': collection_config
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update_commit_msg', methods=['POST'])
def update_commit_msg():
    """Save the commit message of a collection.

    Returns:
        dict: The status of the operation.
    """
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        if (root_path / data['database_name'] / 'commit_msg.json').exists():
            with open(root_path / data['database_name'] / 'commit_msg.json', 'r') as file:
                commit_msg = json.load(file)
                commit_msg[data['collection_name']] = data
        else:
            commit_msg = {data['collection_name']: data}

        with open(root_path / data['database_name'] / 'commit_msg.json', 'w') as file:
            json.dump(commit_msg, file)

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name']
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_commit_msg', methods=['POST'])
def get_commit_msg():
    """Get the commit message of a collection.

    Returns:
        dict: The status of the operation.
    """
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        if (root_path / data['database_name'] / 'commit_msg.json').exists():
            with open(root_path / data['database_name'] / 'commit_msg.json', 'r') as file:
                commit_msg = json.load(file)
                commit_msg = commit_msg.get(data['collection_name'], None)
        else:
            commit_msg = 'No commit message found for this collection'

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'], 'commit_msg': commit_msg
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update_collection_description', methods=['POST'])
def update_collection_description():
    """Update the description of a collection.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        my_vec_db.update_collection_description(data['collection_name'], data['description'])

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'], 'description': data['description']
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update_description', methods=['POST'])
def update_description():
    """Update the description of the database.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])
        collection.update_description(data['description'])

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'],
            'description': data['description']
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/show_collections_details', methods=['POST'])
def show_collections_details():
    """Show all collections in the database with details.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collections_details = my_vec_db.show_collections_details()
        return Response(json.dumps({
            'status': 'success', 'params': {
                'database_name': data['database_name'],
                'collections': collections_details.to_dict()
            }
        },
            sort_keys=False), mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/build_index', methods=['POST'])
def build_index():
    """Build the index of a collection.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])
        collection.build_index(index_mode=data.get('index_mode', 'IVF-FLAT'))

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'], 'index_mode': data.get('index_mode', 'IVF-FLAT')
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/remove_index', methods=['POST'])
def remove_index():
    """Remove the index of a collection.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])
        collection.remove_index()

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name']
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/list_databases', methods=['GET'])
def list_databases():
    """List all databases.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.database_manager import DatabaseManager

    try:
        data_manager = DatabaseManager(root_path_parent)
        databases = data_manager.list_database()
        return Response(json.dumps({'status': 'success', 'params': {'databases': databases}}, sort_keys=False),
                        mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete_database', methods=['POST'])
def delete_database():
    """Delete a database.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.database_manager import DatabaseManager

    data = request.json
    try:
        data_manager = DatabaseManager(root_path_parent)
        data_manager.delete(data['database_name'])
        return Response(json.dumps({'status': 'success', 'params': {'database_name': data['database_name']}},
                                   sort_keys=False), mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/create_database', methods=['POST'])
def create_database():
    """Create a database.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.database_manager import DatabaseManager
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    try:
        data_manager = DatabaseManager(root_path_parent)
        data_manager.register(data['database_name'])

        if data['drop_if_exists']:
            LocalClient(root_path=root_path / data['database_name']).drop_database()

        LocalClient(root_path=root_path / data['database_name'])
        return Response(json.dumps({'status': 'success', 'params': {'database_name': data['database_name']}},
                                   sort_keys=False), mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/head', methods=['POST'])
def head():
    """Get the first n items of a collection.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'n' not in data:
        data['n'] = 5

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])
        head = collection.head(n=data['n'])
        head = (head[0].tolist(), head[1].tolist(), head[2])

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'], 'head': head
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tail', methods=['POST'])
def tail():
    """Get the last n items of a collection.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'n' not in data:
        data['n'] = 5

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])
        tail = collection.tail(n=data['n'])
        tail = (tail[0].tolist(), tail[1].tolist(), tail[2])

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'], 'tail': tail
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/read_by_only_id', methods=['POST'])
def read_by_only_id():
    """Read the item by only id.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])
        vector, id, field = collection.read_by_only_id(data['id'])
        vector = vector.tolist()
        id = id.tolist()

        item = (vector, id, field)
        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'], 'item': item
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_collection_path', methods=['POST'])
def get_collection_path():
    """Get the path of a database.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'],
            'collection_path': collection._database_path}}, sort_keys=False), mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/query', methods=['POST'])
def query():
    """Query the database.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])

        result = collection.query(data['filter_instance'], data['filter_ids'], data['return_ids_only'])

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'],
            'result': result}}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/build_field_index', methods=['POST'])
def build_field_index():
    """Build the index of a field.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])

        schema = IndexSchema().load_from_json(data['schema'])

        collection.build_field_index(schema=schema,
                                     rebuild_if_exists=data['rebuild_if_exists'])

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name']
        }}, sort_keys=False), mimetype='application/json')
    except KeyError as e:
        return jsonify({'error': f'Missing required parameter {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/list_field_index', methods=['POST'])
def list_field_index():
    """List all field indexes of a collection.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])

        field_indices = collection.list_field_index()

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'],
            'field_indices': field_indices}}, sort_keys=False), mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/remove_field_index', methods=['POST'])
def remove_field_index():
    """Remove the index of a field.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])

        collection.remove_field_index(data['field_name'])

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name'],
            'field_name': data['field_name']
        }}, sort_keys=False), mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/remove_all_field_indices', methods=['POST'])
def remove_all_field_indices():
    """Remove all field indices of a collection.

    Returns:
        dict: The status of the operation.
    """
    from lynse.api.native_api.high_level import LocalClient

    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        my_vec_db = LocalClient(root_path=root_path / data['database_name'])
        collection = my_vec_db.get_collection(data['collection_name'])

        collection.remove_all_field_indices()

        return Response(json.dumps({'status': 'success', 'params': {
            'database_name': data['database_name'],
            'collection_name': data['collection_name']
        }}, sort_keys=False), mimetype='application/json')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        return "127.0.0.1"


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Start the LynseDB HTTP API server.')
    parser.add_argument('--host', default='127.0.0.1', help='The host to bind to.')
    parser.add_argument('--port', default=7637, type=int, help='The port to bind to.')
    parser.add_argument('--threads', default=10, type=int, help='Number of threads per worker.')
    parser.add_argument('run', help='Run the server.')
    args = parser.parse_args()

    if args.run:
        if args.host == '0.0.0.0':
            local_ip = get_local_ip()
            print(f"Server running at:")
            print(f"  - Localhost: http://localhost:{args.port}")
            print(f"  - Local IP: http://{local_ip}:{args.port}", end="\n\n")
        else:
            print(f"Server running at http://{args.host}:{args.port}", end="\n\n")

        serve(app, host=args.host, port=args.port, threads=args.threads)


def launch_in_jupyter(host: str = '127.0.0.1', port: int = 7637, threads: int = 10):
    """
    Launch the HTTP API server in Jupyter notebook.

    Parameters:
        host (str): The host to bind to. Default is '127.0.0.1'
        port (int): The port to bind to. Default is 7637.
        threads (int): Number of threads per worker. Default is 10.

    Returns:
        None
    """
    # use another thread to start the server
    import threading
    if host == '0.0.0.0':
        local_ip = get_local_ip()
        print(f"Server running at:")
        print(f"  - Localhost: http://localhost:{port}")
        print(f"  - Local IP: http://{local_ip}:{port}", end="\n\n")
    else:
        print(f"Server running at http://{host}:{port}", end="\n\n")

    # set the thread as daemon thread
    server_thread = threading.Thread(target=serve, args=(app,), kwargs={'host': host, 'port': port, 'threads': threads})
    server_thread.daemon = True
    server_thread.start()


if __name__ == '__main__':
    main()
