# coding: utf-8
# Copyright 2009 Alexandre Fiori
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pymonga import wire
from pymonga._pymongo.objectid import ObjectId
from twisted.internet import defer, reactor, protocol

"""An asynchronous Mongo driver for Python."""

def Connection(host="localhost", port=27017):
    cli = protocol.ClientCreator(reactor, wire.MongoProtocol)
    return cli.connectTCP(host, port)

def ConnectionPool(host="localhost", port=27017, size=5):
    def wrapper(connections):
        size = len(connections)
        for cli in connections:
            cli._set_pool(connections, size)
        return cli

    conn = []
    for x in xrange(size):
        conn.append(Connection(host, port))

    deferred = defer.gatherResults(conn)
    deferred.addCallback(wrapper)
    return deferred
