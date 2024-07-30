import asyncio
import os

from dapr.actor import ActorProxyFactory, ActorProxy, ActorId
from flask import Flask, render_template, request, jsonify

from smartbulb_actor_interface import SmartBulbActorInterface

app = Flask(__name__)


@app.route("/")
def home():
    namespace = os.getenv('NAMESPACE') or 'default'
    factory = ActorProxyFactory()

    status = {}
    for id in ["bulb1", "bulb2", "bulb3"]:
        proxy = ActorProxy.create('SmartBulbActor', ActorId(id), SmartBulbActorInterface, factory)
        rtn_obj = asyncio.run(proxy.GetMyData())
        status[id] = rtn_obj.get("status", False) if rtn_obj else False

    return render_template('index.html', namespace=namespace, status=status, title=f"Client app - {namespace}")


@app.route('/update_bulb', methods=['POST'])
def update_bulb():
    data = request.json
    bulb_id = data['bulb_id']
    status = data['status']
    print(f"Bulb {bulb_id} is now {'on' if status else 'off'}")

    factory = ActorProxyFactory()
    proxy = ActorProxy.create('SmartBulbActor', ActorId(bulb_id), SmartBulbActorInterface, factory)

    rtn_obj = asyncio.run(proxy.SetMyData({'status': status}))
    print(rtn_obj, flush=True)

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
