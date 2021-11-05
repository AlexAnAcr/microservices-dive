from flask import Flask, request, jsonify
import threading
import time
import datetime

storage = []
mutex = threading.Lock()

def storage_add(json):
    mutex.acquire()
    storage.append(json)
    mutex.release()

def storage_find(type, id):
    mutex.acquire()
    result = None
    if type == 'null':
        for item in storage:
            if item['visibleId'] and item['id'] == id:
                result = item
                storage.remove(item)
                break;
    elif id == 'null':
        for item in storage:
            if item['type'] == type:
                result = item
                storage.remove(item)
                break;
    else:
        for item in storage:
            if item['visibleId'] and item['type'] == type and item['id'] == id:
                result = item
                storage.remove(item)
                break;
    mutex.release()
    return result

app = Flask(__name__)

@app.route('/got', methods=["GET"])
def jobGet():
    needType = request.values.get('type')
    if needType == None:
        needType = 'null'

    needId = request.values.get('id')
    if needId == None:
        needId = 'null'

    result = None
    end_time = start_time = datetime.datetime.now()
    while (end_time - start_time).seconds < 25:
        result = storage_find(needType, needId)
        if result != None:
            break;
        time.sleep(1)
        end_time = datetime.datetime.now()

    if result == None:
        return '',408
    else:
        return jsonify(result)

@app.route('/gave', methods=["POST"])
def jobPost():
    storage_add(request.get_json())
    return '',201

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
