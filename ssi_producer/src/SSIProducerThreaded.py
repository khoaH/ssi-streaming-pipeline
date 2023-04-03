import websocket
import time
import threading
from kafka import KafkaProducer
import json

class SSIProducerThreaded:
    def __init__(self):
        with open('settings.json', 'r') as f:
            self.settings = json.load(f)
        self.ws_url = "wss://pricestream-iboard.ssi.com.vn/realtime"
        self.topic = self.settings['kafka_topic']
        self.producer = KafkaProducer(bootstrap_servers=self.settings['kafka_server'])
        # self.lock = threading.Lock
        self.messages_queue = []
        self.ws = None
        with open('symbols_dict.txt') as f:
            syms_dict = json.load(f)
        stock_list = [syms_dict[symbol] for symbol in self.settings['tickers']]
        self.stock_list = '["' + '","'.join(stock_list) + '"]'
        self.ws = websocket.WebSocketApp(self.ws_url,
                                    on_close=self.on_close,
                                    on_open=self.on_open,
                                    on_error=self.on_error,
                                    on_message=self.on_message)
        self.ws.run_forever()

    def run(self):
        # self.ws = websocket.WebSocketApp(self.ws_url, 
        #                                  on_close=lambda ws: self.on_close(),
        #                                  on_error=lambda ws, error: self.on_error(error),
        #                                  on_message=lambda ws, message: self.on_message(message),
        #                                  on_open=lambda ws: self.on_open())
        # ws_thread = threading.Thread(target=lambda: self.ws.run_forever())
        # ws_thread.daemon = True
        # ws_thread.start()
        # ws_thread.join()
        self.ws = websocket.WebSocketApp(self.ws_url,
                                         on_close=self.on_close,
                                         on_open=self.on_open,
                                         on_error=self.on_error,
                                         on_message=self.on_message)
        self.ws.run_forever()

    def on_message(self, ws_url, message):
        timestamp = str(time.time())
        if message[:2] == 'S#':
            # with self.lock:
            data = json.dumps({"timestamp":timestamp, "message":message})
            self.producer.send(topic=self.topic, value=data.encode('utf-8'))
            # self.messages_queue.append(data)
            # while len(self.messages_queue) > 0:
            #     data = self.messages_queue[0]
            #     if time.time() - data["timestamp"] > 1:
            #         self.producer.send(topic=self.topic, value=data.encode('utf-8'))
            #         self.messages_queue.pop(0)
            #     else:
            #         break
        else:
            print(message)
    
    def on_open(self, ws_url):
        print("Websocket connection opened.")
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
    # producer.run()
    