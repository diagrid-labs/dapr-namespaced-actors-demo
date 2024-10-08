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

from abc import abstractmethod

from dapr.actor import ActorInterface, actormethod


class SmartBulbActorInterface(ActorInterface):
    @abstractmethod
    @actormethod(name='GetStatus')
    async def get_status(self) -> object:
        ...

    @abstractmethod
    @actormethod(name='SetStatus')
    async def set_status(self, data: object) -> None:
        ...

    @abstractmethod
    @actormethod(name='SetReminder')
    async def set_reminder(self, enabled: bool) -> None:
        ...

    @abstractmethod
    @actormethod(name='SetTimer')
    async def set_timer(self, enabled: bool) -> None:
        ...

    @abstractmethod
    @actormethod(name='GetReentrancyStatus')
    async def get_reentrancy_status(self) -> bool:
        ...
