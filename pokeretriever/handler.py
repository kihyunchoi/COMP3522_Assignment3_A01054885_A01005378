import abc
from pokeretriever import request, aiohttp, pokedex_object
import io
import json
import pickle

class BaseHandler(abc.ABC):

    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abc.abstractmethod
    def handle_request(self, req: request.Request):
        pass

    def set_handler(self, handler):
        self.next_handler = handler


class ErrorHandler:
    @staticmethod
    def handle_error(error):
        print(error)


class ModeHandler(BaseHandler):

    def handle_request(self, req: request.Request):
        if req.mode is not None:
            if req.mode == "pokemon" or req.mode == "ability" or req.mode == "move":
                self.set_handler(InputHandler)
                return self.next_handler.handle_request(InputHandler, req)
            else:
                return ErrorHandler.handle_error(f"{req}\n mode is not provided."
                                                 "Choose one of pokemon | ability | move")
        else:
            return ErrorHandler.handle_error("No mode provided."
                                             " Choose one of pokemon | ability | move")


class InputHandler(BaseHandler):

    def handle_request(self, req: request.Request):
        if (req.input_file is not None and ".txt" in req.input_file) or (req.input_data is not None):
            self.set_handler(self, ExpandedHandler)
            return self.next_handler.handle_request(ExpandedHandler, req)
        else:
            return ErrorHandler.handle_error("File or data is not provided")


class ExpandedHandler(BaseHandler):

    def handle_request(self, req: request.Request):
        if req.expanded is True:
            if req.mode.lower() == "pokemon":
                self.set_handler(self, OutputHandler)
                return self.next_handler.handle_request(self, req)
            else:
                return ErrorHandler.handle_error(f"{req}\n"
                                                 f"Expanded is only available for mode=Pokemon")
        else:
            self.set_handler(self, OutputHandler)
            return self.next_handler.handle_request(OutputHandler, req)


class OutputHandler(BaseHandler):

    @staticmethod
    async def create_object(req: request.Request):
        mode = req.mode.lower()
        json_data = await aiohttp.process_single_request(mode, req.input_data)
        obj = None
        if mode == "pokemon":
            types = []
            for t in json_data["types"]:
                types.append(t["type"]["name"])

            if req.expanded is True:
                # get abilities
                abilities = []
                ids = []
                for a in json_data["abilities"]:
                    url = a["ability"]["url"].split("/")
                ab_data = await aiohttp.process_single_request("ability", url[6])
                pokemon_names = []
                for d in ab_data["pokemon"]:
                    pokemon_names.append(d["pokemon"]["name"])
                ability = pokedex_object.Ability(ab_data["name"], ab_data["id"], ab_data["generation"]["name"],
                                                 ab_data["effect_entries"][0]["effect"],
                                                 ab_data["effect_entries"][0]["short_effect"], pokemon_names)
                abilities.append(ability)

                # get Stats
                stats = []
                for s in json_data["stats"]:
                    url = s["stat"]["url"].split("/")
                    s_data = await aiohttp.process_single_request("stat", url[6])
                    stat = pokedex_object.Stat(s_data["name"], s_data["id"], s_data["is_battle_only"],
                                               s["base_stat"])
                    stats.append(stat)

                # get Moves
                moves = []
                ids = []
                for m in json_data["moves"]:
                    url = m["move"]["url"].split("/")
                    ids.append(url[6])
                m_data = await aiohttp.process_requests("move", ids)
                for mm in m_data:
                    move = pokedex_object.Move(mm["name"], mm["id"], mm["generation"]["name"], mm["accuracy"], mm["pp"],
                                               mm["power"], mm["type"]["name"], mm["damage_class"]["name"],
                                               mm["effect_entries"][0]["short_effect"])

                    moves.append(move)

            else:
                stats = []
                for s in json_data["stats"]:
                    stat = pokedex_object.Stat(name=s["stat"]["name"], base_stat=s["base_stat"])
                    stats.append(stat)

                abilities = []
                for a in json_data["abilities"]:
                    ab = pokedex_object.Ability(name=a["ability"]["name"])
                    abilities.append(ab)

                moves = []
                for m in json_data["moves"]:
                    move = pokedex_object.Move(name=m["move"]["name"],
                                               level=m["version_group_details"][0]["level_learned_at"])
                    moves.append(move)

            # create Pokemon object
            obj = pokedex_object.Pokemon(json_data["name"], json_data["id"], json_data["height"],
                                         json_data["weight"], stats, types, abilities, moves)
        elif mode == "ability":
            pokemon = []
            for p in json_data["pokemon"]:
                pokemon.append(p["pokemon"]["name"])
            obj = pokedex_object.Ability(json_data["name"], json_data["id"], json_data["generation"]["name"],
                                         json_data["effect_entries"][0]["effect"],
                                         json_data["effect_entries"][0]["short_effect"], pokemon)
        elif mode == "move":
            obj = pokedex_object.Move(json_data["name"], json_data["id"], json_data["generation"]["name"],
                                      json_data["accuracy"], json_data["pp"], json_data["power"],
                                      json_data["type"]["name"], json_data["damage_class"]["name"],
                                      json_data["effect_entries"][0]["short_effect"])
        return obj

    @staticmethod
    async def create_objects(req: request.Request):
        mode = req.mode.lower()
        from_file = req.input_file

        lines = []
        try:
            with open(from_file, mode="r") as file:
                for raw in file:
                    lines.append(raw.lower().strip())
            file.close()

        except FileNotFoundError:
            return f"File '{from_file}' could not be found."

        json_data = await aiohttp.process_requests(mode, lines)
        obj = None

        if mode == "pokemon":
            pokemon_objects = []
            for pokemon in json_data:
                if pokemon is None:
                    continue
                types = []
                for t in pokemon["types"]:
                    types.append(t["type"]["name"])

                if req.expanded is True:
                    # get abilities
                    abilities = []
                    ids = []
                    for a in pokemon["abilities"]:
                        url = a["ability"]["url"].split("/")
                    ab_data = await aiohttp.process_single_request("ability", url[6])
                    pokemon_names = []
                    for d in ab_data["pokemon"]:
                        pokemon_names.append(d["pokemon"]["name"])
                    ability = pokedex_object.Ability(ab_data["name"], ab_data["id"], ab_data["generation"]["name"],
                                                     ab_data["effect_entries"][0]["effect"],
                                                     ab_data["effect_entries"][0]["short_effect"], pokemon_names)
                    abilities.append(ability)

                    # get Stats
                    stats = []
                    for s in pokemon["stats"]:
                        url = s["stat"]["url"].split("/")
                        s_data = await aiohttp.process_single_request("stat", url[6])
                        stat = pokedex_object.Stat(s_data["name"], s_data["id"], s_data["is_battle_only"],
                                                   s["base_stat"])
                        stats.append(stat)

                    # get Moves
                    moves = []
                    ids = []
                    for m in pokemon["moves"]:
                        url = m["move"]["url"].split("/")
                        ids.append(url[6])
                    m_data = await aiohttp.process_requests("move", ids)
                    for mm in m_data:
                        move = pokedex_object.Move(mm["name"], mm["id"], mm["generation"]["name"], mm["accuracy"], mm["pp"],
                                                   mm["power"], mm["type"]["name"], mm["damage_class"]["name"],
                                                   mm["effect_entries"][0]["short_effect"])

                        moves.append(move)

                else:
                    stats = []
                    for s in pokemon["stats"]:
                        stat = pokedex_object.Stat(name=s["stat"]["name"], base_stat=s["base_stat"])
                        stats.append(stat)

                    abilities = []
                    for a in pokemon["abilities"]:
                        ab = pokedex_object.Ability(name=a["ability"]["name"])
                        abilities.append(ab)

                    moves = []
                    for m in pokemon["moves"]:
                        move = pokedex_object.Move(name=m["move"]["name"],
                                                   level=m["version_group_details"][0]["level_learned_at"])
                        moves.append(move)

                # create Pokemon object
                obj = pokedex_object.Pokemon(pokemon["name"], pokemon["id"], pokemon["height"],
                                             pokemon["weight"], stats, types, abilities, moves)
                pokemon_objects.append(obj)

        elif mode == "ability":
            pokemon = []
            for p in json_data["pokemon"]:
                pokemon.append(p["pokemon"]["name"])
            obj = pokedex_object.Ability(json_data["name"], json_data["id"], json_data["generation"]["name"],
                                         json_data["effect_entries"][0]["effect"],
                                         json_data["effect_entries"][0]["short_effect"], pokemon)
        elif mode == "move":
            obj = pokedex_object.Move(json_data["name"], json_data["id"], json_data["generation"]["name"],
                                      json_data["accuracy"], json_data["pp"], json_data["power"],
                                      json_data["type"]["name"], json_data["damage_class"]["name"],
                                      json_data["effect_entries"][0]["short_effect"])
        return pokemon_objects

    async def handle_request(self, req: request.Request):
        print("Handling Output")
        if req.input_file is not None:
            poke_objects = await OutputHandler.create_objects(req)
            if req.output == "print":
                return poke_objects
            else:
                result = poke_objects
                with open(req.output, 'w') as f:
                    for item in result:
                        f.write("%s\n" % item)
                return f"{req.input_file} is Written to {req.output}"
        elif req.input_data is not None:
            poke_object = await OutputHandler.create_object(req)
            if req.output == "print":
                return poke_object
            else:
                try:
                    with open(req.output, 'w', -1, "utf-8") as file:
                        for line in (str(poke_object).split('\n')):
                            file.write(line + "\n")
                    return f"\nmode:{req.mode} / id:{req.input_data} is Written to {req.output}\n"

                except FileNotFoundError:
                    return f"{req.input_data} could not written to {req.output}"
        else:
            return ErrorHandler.handle_error("Output cannot be provided. "
                                             "No input file or input data")
