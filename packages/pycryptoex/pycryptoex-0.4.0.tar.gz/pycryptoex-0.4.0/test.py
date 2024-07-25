import sys
import logging
sys.dont_write_bytecode = True

from clients.kucoin import KuCoin

import asyncio


logging.basicConfig(level="DEBUG")


async def main():
    exchange = KuCoin(
        api_key="667e97b20e0f3800011e4704",
        secret="224077e3-ec0d-4b7f-8f57-bca43771d7f5",
        passphrase="Gupeboner18"
    )
    async with exchange:
        # print(await exchange.request(
        #     path="/api/v2/user-info",
        #     signed=True
        # ))

        async def handler(json_data):
            print(json_data)

        ws = await exchange.create_websocket_stream(private=True)
        await ws.start()
        await asyncio.sleep(3)
        await ws.subscribe_callback("/market/candles:BTC-USDT_1min", handler)
        print(ws.subscriptions)
        await asyncio.sleep(3)
        await ws.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
