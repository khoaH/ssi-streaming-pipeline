import websocket
import time
import threading
from kafka import KafkaProducer
import json

class SSIProducerThreaded:
    def __init__(self):
        #load settings and add to configurations
        with open('settings.json', 'r') as f:
            self.settings = json.load(f)
        self.ws_url = "wss://pricestream-iboard.ssi.com.vn/realtime"
        self.topic = self.settings['kafka_topic']
        self.producer = KafkaProducer(bootstrap_servers=self.settings['kafka_server'])
        self.ws = None

        #get tickers id to subscribe to ws
        with open('symbols_dict.txt') as f:
            syms_dict = json.load(f)
        stock_list = [syms_dict[symbol] for symbol in self.settings['tickers']]
        self.stock_list = '["' + '","'.join(stock_list) + '"]'
        
        #run the app
        self.ws = websocket.WebSocketApp(self.ws_url,
                                    on_close=self.on_close,
                                    on_open=self.on_open,
                                    on_error=self.on_error,
                                    on_message=self.on_message)
        self.ws.run_forever()

    def on_message(self, ws_url, message):
        #get current time, wrap with the message and push to kafka
        timestamp = str(time.time())
        if message[:2] == 'S#':
            data = json.dumps({"timestamp":timestamp, "message":message})
            self.producer.send(topic=self.topic, value=data.encode('utf-8'))
        else:
            print(message)
    
    def on_open(self, ws_url):
        print("Websocket connection opened.")
        #websocket initilizing and subscribe to tickers 
        self.ws.send('{"type":"init"}')
        self.ws.send('{"type":"sub","topic":"serverName"}')
        self.ws.send('{"type":"sub","topic":"stockRealtimeByList","variables":' + self.stock_list + '}')

    def on_error(self, ws_url, e):
        print(f'WebSocket Error: {e}')
    
    def on_close(wsapp, ws_url, close_status_code, close_msg):
        print('### Websocket Closed ###')
        print(close_msg)

if __name__ == "__main__":
    SSIProducerThreaded()
    