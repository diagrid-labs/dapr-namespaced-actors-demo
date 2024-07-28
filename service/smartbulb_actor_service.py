# -*- coding: utf-8 -*-
# Copyright 2021 The Dapr Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import asyncio
import os

from dapr.actor import ActorProxyFactory, ActorProxy, ActorId
from fastapi import FastAPI, Request  # type: ignore
from fastapi.responses import HTMLResponse  # type: ignore
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dapr.actor.runtime.config import ActorRuntimeConfig, ActorTypeConfig, ActorReentrancyConfig
from dapr.actor.runtime.runtime import ActorRuntime
from dapr.ext.fastapi import DaprActor  # type: ignore

from smartbulb_actor_interface import SmartBulbActorInterface
from smartbulb_actor import SmartBulbActor


app = FastAPI(title=f'{SmartBulbActor.__name__}Service')

# This is an optional advanced configuration which enables reentrancy only for the
# specified actor type. By default reentrancy is not enabled for all actor types.
config = ActorRuntimeConfig()  # init with default values
config.update_actor_type_configs(
    [ActorTypeConfig(actor_type=SmartBulbActor.__name__, reentrancy=ActorReentrancyConfig(enabled=True))]
)
ActorRuntime.set_actor_config(config)

# Add Dapr Actor Extension
actor = DaprActor(app)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event('startup')
async def startup_event():
    # Register SmartBulbActor
    await actor.register_actor(SmartBulbActor)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    namespace = os.getenv('NAMESPACE') or 'default'
    print(f'-----------------------namespace: {namespace}', flush=True)

    factory = ActorProxyFactory()
    proxy = ActorProxy.create('SmartBulbActor', ActorId("bulb1"), SmartBulbActorInterface, factory)

    rtn_obj = await proxy.GetMyData()

    status = {}
    for id in ["bulb1", "bulb2", "bulb3"]:
        proxy = ActorProxy.create('SmartBulbActor', ActorId(id), SmartBulbActorInterface, factory)
        rtn_obj = await proxy.GetMyData()
        status[id] = rtn_obj.get("status", False) if rtn_obj else False


    # status = {"bulb1": True, "bulb2": False, "bulb3": True}


    # return templates.TemplateResponse(request=request, name="index.html", context={"namespace": namespace})
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "title": f"{SmartBulbActor.__name__}Service - {namespace}",
                                                     "namespace": namespace,
                                                     "status": status})

