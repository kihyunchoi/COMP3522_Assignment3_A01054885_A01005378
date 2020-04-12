from pokeretriever.handler import ModeHandler
from pokeretriever.pokedex_object import PokedexObject
from pokeretriever.request import Request, setup_request_commandline


class PokedexFacade:

    def __init__(self):
        self.start_handler = ModeHandler()

    def execute_request(self, req: Request) -> PokedexObject:
        result = self.start_handler.handle_request(req)
        print(result)


def main(req: Request):
    aiohttp = PokedexFacade()
    aiohttp.execute_request(req)


if __name__ == '__main__':
    request = setup_request_commandline()
    main(request)
