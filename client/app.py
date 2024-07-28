# import asyncio
#
# from dapr.actor import ActorProxy, ActorId, ActorProxyFactory
# from smartbulb_actor_interface import SmartBulbActorInterface
#
#
# async def main():
#     # Create proxy client
#     factory = ActorProxyFactory()
#     proxy = ActorProxy.create('SmartBulbActor', ActorId('1'), SmartBulbActorInterface, factory)
#
#     # -----------------------------------------------
#     # Actor invocation demo
#     # -----------------------------------------------
#     # non-remoting actor invocation
#     print('call actor method via proxy.invoke_method()', flush=True)
#     rtn_bytes = await proxy.invoke_method('GetMyData')
#     print(rtn_bytes, flush=True)
#     # RPC style using python duck-typing
#     print('call actor method using rpc style', flush=True)
#     rtn_obj = await proxy.GetMyData()
#     print(rtn_obj, flush=True)
#
# asyncio.run(main())

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

    rtn_obj = asyncio.run(proxy.SetMyData({'status': status}))
    print(rtn_obj, flush=True)

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
