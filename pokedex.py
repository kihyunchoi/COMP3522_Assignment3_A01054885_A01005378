from pokeretriever.handler import ModeHandler
from pokeretriever.pokedex_object import PokedexObject
from pokeretriever.request import Request, setup_request_commandline
import asyncio


class PokedexFacade:

    def __init__(self):
        self.start_handler = ModeHandler()

    def execute_request(self, req: Request) -> PokedexObject:
        result = self.start_handler.handle_request(req)
        return result


async def main(req: Request):
    aiohttp = PokedexFacade()
    result = await aiohttp.execute_request(req)
    print(result)
    print(req)


if __name__ == '__main__':
    request = setup_request_commandline()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Blocking call which returns when the hello_world() coroutine is done
    loop.run_until_complete(main(request))
