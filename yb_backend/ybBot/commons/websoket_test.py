import json
import asyncio
import websockets
import ssl
import certifi



ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())


async def upbit_websoket():

     wb = await websockets.connect("wss://api.upbit.com/websocket/v1", ping_interval=None,ssl=ssl_context)
     await wb.send(json.dumps([{"ticket":"UNIQUE_TICKET"},{"type":"orderbook","codes":["KRW-BTC","BTC-XRP"]}]))
     
     while True:
          if wb.open:
               result = await wb.recv()
               result = json.loads(result)
               print(result)
          else:
               print('연결 안됨! 또는 연결 끊김')


loop = asyncio.get_event_loop()
asyncio.ensure_future(upbit_websoket())
loop.run_forever()