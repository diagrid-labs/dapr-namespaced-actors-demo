import asyncio

from dapr.actor import ActorProxyFactory, ActorProxy, ActorId
from flask import Flask, render_template, request, jsonify

from smartbulb_actor_interface import SmartBulbActorInterface

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/update_bulb', methods=['POST'])
def update_bulb():
    data = request.json
    bulb_id = data['bulb_id']
    status = data['status']
    # Here you can handle the update, e.g., store it in a database or perform an action
    print(f"Bulb {bulb_id} is now {'on' if status else 'off'}")

    factory = ActorProxyFactory()
    proxy = ActorProxy.create('SmartBulbActor', ActorId(bulb_id), SmartBulbActorInterface, factory)

    # rtn_obj = proxy.GetMyData()
    rtn_obj = asyncio.run(proxy.invoke_method('get_my_data'))
    print(rtn_obj, flush=True)

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
