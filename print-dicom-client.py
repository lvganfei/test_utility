#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(pika.URLParameters("amqp://democompany:123456@127.0.0.1:7003/"))
channel = connection.channel()

message = {
    'type': 0,
    'createTime': '2021-03-22 17:47:51',
    'appName': 'test',
    'taskId': 'task1',
    'value': None
}
data = {
    'aeInfo': {
        'host': '10.10.10.102',
        'port': 104,
        'aeTitle': 'PRINTSCP11'
    },
    'template': {},
    'workspace': '/Users/chenliang/workspace/dcm/original/print',
    'filmSize': '14INX17IN',
    'colorType': 'MONO'
}
message['value'] = data
channel.basic_publish(exchange="print-dicom-plugin-exchange",
                      routing_key="net.democompany.plugin.print",
                      body=json.dumps(message))
