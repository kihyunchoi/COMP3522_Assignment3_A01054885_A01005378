"""
This module depicts the use of asyncio and aiohttp to make HTTP GET
requests.
"""
import aiohttp
import asyncio


async def get_pokemon_data(mode: str, id_: int, url: str, session: aiohttp.ClientSession) -> dict:
    """
    An async coroutine that executes GET http request. The response is
    converted to a json. The HTTP request and the json conversion are
    asynchronous processes that need to be awaited.
    :param mode:
    :param id_: an int
    :param url: a string, the unformatted url (missing parameters)
    :param session: a HTTP session
    :return: a dict, json representation of response.
    """
    target_url = url.format(mode, id_)
    response = await session.request(method="GET", url=target_url)
    # print("Response object from aiohttp:\n", response)
    # print("Response object type:\n", type(response))
    # print("-----")
    json_dict = await response.json()
    return json_dict


async def process_single_request(mode, id_) -> dict:
    """
    This function depicts the use of await to showcase how one async
    coroutine can await another async coroutine
    :param mode:
    :param id_: an int
    :return: dict, json response
    """
    url = "https://pokeapi.co/api/v2/{}/{}/"
    async with aiohttp.ClientSession() as session:
        response = await get_pokemon_data(mode, id_, url, session)
        # print(response)
        return response


async def process_requests(mode: str, requests: list) -> list:
    """
    This function depicts the use of asyncio.gather to run multiple
    async coroutines concurrently.
    :param mode:
    :param requests: a list of int's
    :return: list of dict, collection of response data from the endpoint.
    """
    url = "https://pokeapi.co/api/v2/{}/{}/"
    async with aiohttp.ClientSession() as session:
        async_coroutines = [get_pokemon_data(mode, id_, url, session)
                            for id_ in requests]

        responses = await asyncio.gather(*async_coroutines)
        return responses


async def process_single_request_task(mode: str, id_: int) -> list:
    """
    Thsi function depicts how an async coroutine can be converted into
    a task object and awaited.
    :param mode:
    :param id_: an int
    :return:
    """
    url = "https://pokeapi.co/api/v2/{}/{}/"
    async with aiohttp.ClientSession() as session:
        print("***process_single_request_task")
        coroutine = get_pokemon_data(mode, id_, url, session)
        async_task = asyncio.create_task(coroutine)
        response = await async_task
        print(response)
        return response


async def process_requests_tasks(mode: str, requests: list) -> list:
    """
    This function depicts the use of asyncio.gather to run multiple
    async tasks concurrently.
    :param mode:
    :param requests: a list of int's
    :return: list of dict, collection of response data from the endpoint.
    """
    url = "https://pokeapi.co/api/v2/{}/{}/"
    async with aiohttp.ClientSession() as session:
        print("***process_requests_tasks")
        list_tasks = [asyncio.create_task(get_pokemon_data(mode, id_, url, session))
                      for id_ in requests]
        responses = await asyncio.gather(*list_tasks)
        for response in responses:
            print(response)
        return responses


# def main():
#
#     loop = asyncio.get_event_loop()
#
#     # response = loop.run_until_complete(process_single_request("pokemon", 1))
#     # response2 = loop.run_until_complete(process_single_request("ability", 2))
#     # response3 = loop.run_until_complete(process_single_request_task("type", 3))
#     requests = [1, 2, 3, 4, 5]
#     responses = loop.run_until_complete(process_requests("pokemon", requests))
#     responses1 = loop.run_until_complete(process_requests("ability", requests))
#     responses2 = loop.run_until_complete(process_requests_tasks("move", requests))
#     print()
#     response = loop.run_until_complete(process_single_request("pokemon", 1))
#     response2 = loop.run_until_complete(process_single_request("ability", 2))
#     response3 = loop.run_until_complete(process_single_request_task("type", 3))
#
#
# if __name__ == '__main__':
#     main()
