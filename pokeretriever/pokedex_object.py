import abc
import textwrap


class PokedexObject(abc.ABC):
    def __init__(self, name, _id=None):
        self.name = name
        self._id = _id


class Pokemon(PokedexObject):
    def __init__(self, name, _id, height, weight, stats, types, abilities, moves):
        """
        Create a Pokemon.
        :param name: String
        :param _id: int
        :param height: int
        :param weight: int
        :param stats: List(Stat), expandable
        :param types: List(String)
        :param abilities: List(Ability), expandable
        :param moves: List(Move), expandable
        """
        super().__init__(name, _id)
        self.height = height
        self.weight = weight
        self.stats = stats
        self.types = types
        self.abilities = abilities
        self.moves = moves

    def get_id(self):
        return self._id

    def __str__(self):
        width = 80
        stats = ""
        for s in self.stats:
            stats += "\n" + s.__str__() + "-" * width

        moves = ""
        for m in self.moves:
            moves += "\n" + m.__str__()

        abilities = ""
        for a in self.abilities:
            abilities += "\n" + a.__str__()

        stri = '+-' + '-' * width + '-+'
        stri += '\n| {0:^{1}} |'.format("Pokemon Details", width)
        stri += '\n+-' + '-' * width + '-+'
        type_str = ", ".join(self.types)
        poke_str = "\n{:<15} {:<20}".format("Pokemon Name:", self.name)
        poke_str += "\n{:<15} {:<20}".format("Pokedex ID:", self.get_id())
        height = str(self.height) + " decimetres"
        poke_str += "\n{:<15} {:<20}".format("Height:", height)
        weight = str(self.weight) + " hectograms"
        poke_str += "\n{:<15} {:<20}".format("Weight:", weight)
        poke_str += "\n{:<15} {:<20}".format("Types:", type_str)
        msg = textwrap.indent(text=poke_str, prefix='+ ', predicate=lambda line: True)
        mylist = [textwrap.fill(i, width=width) for i in msg.split('\n') if i != "+ "]
        joined = "\n".join(mylist)
        splitted = joined.split("\n")
        for i in splitted:
            stri += '\n| {0:{1}} |'.format(i, width)

        # Formatting Stats
        stri += '\n+-' + '-' * width + '-+'
        stri += '\n| {0:^{1}} |'.format("Stats", width)
        stri += '\n+-' + '-' * width + '-+'

        wrapper = textwrap.TextWrapper(width=width)
        mylist = [wrapper.wrap(i) for i in stats.split('\n') if i != '']
        for i in mylist:
            stri += '\n| {0:{1}} |'.format(i[0], width)

        # str += '\n+-' + '-' * (width) + '-+'

        # Formatting Abilities
        stri += '\n+-' + '-' * width + '-+'
        stri += '\n| {0:^{1}} |'.format("Abilities", width)
        stri += abilities

        # Formatting Moves
        stri += '\n+-' + '-' * width + '-+'
        stri += '\n| {0:^{1}} |'.format("Moves", width)
        stri += moves + "\n\n"

        return stri


class Ability(PokedexObject):
    def __init__(self, name, _id=None, generation=None, effect=None, effect_short=None, pokemon=None):
        """
        Store an Ability object.
        :param name: String
        :param _id: int
        :param generation: String
        :param effect: String
        :param effect_short: String
        :param pokemon: List(String), names of the pokemon
        """
        super().__init__(name, _id)
        self.generation = generation
        self.effect = effect
        self.effect_short = effect_short
        self.pokemon = pokemon

    def __str__(self):
        width = 80
        stri = ""
        if self._id is None:
            stri += "Ability Name: {}\n".format(self.name)
        else:
            stri += "Ability Name: {}\nAbility ID: {}\nGeneration: {}\nEffect: {}\nShort Effect: {}\n" \
                   "Pokemons with same ability: {}\n".format(self.name, self._id, self.generation, self.effect,
                                                             self.effect_short, self.pokemon)
        msg = textwrap.indent(text=stri, prefix='+ ', predicate=lambda line: True)
        mylist = [textwrap.fill(i, width=width) for i in msg.split('\n')]
        joined = "\n".join(mylist)
        splitted = joined.split("\n")
        result = '+-' + '-' * width + '-+'
        for i in splitted:
            if i != "":
                result += '\n| {0:{1}} |'.format(i, width)
        return result + '\n+-' + '-' * width + '-+'


class Move(PokedexObject):
    def __init__(self, name, _id=None, generation=None, accuracy=None, pp=None,
                 power=None, types=None, damage_class=None, effect_short=None, level=None):
        """
        Create a Move object.
        :param name: String
        :param _id: int
        :param generation: String
        :param accuracy: int
        :param pp: int
        :param power: int
        :param types: String
        :param damage_class: String
        :param effect_short: String
        """
        super().__init__(name, _id)
        self.generation = generation
        self.accuracy = accuracy
        self.pp = pp
        self.power = power
        self.type = types
        self.damage_class = damage_class
        self.effect_short = effect_short
        self.level = level

    def __str__(self):
        stri = ""
        width = 80
        if self.type is None:
            stri += "Move Name: {}\nLevel Acquired: {}\n".format(self.name, self.level)
        else:
            stri += "Move Name: {}\nMove ID: {}\nGeneration: {}\nAccuracy: {}\nPP: {}\nPower: {}\nType: {}\n" \
                   "Damage Class: {}\nEffect: {}\n".format(self.name, self._id, self.generation, self.accuracy,
                                                           self.pp, self.power, self.type, self.damage_class,
                                                           self.effect_short)

        msg = textwrap.indent(text=stri, prefix='+ ', predicate=lambda line: True)
        mylist = [textwrap.fill(i, width=width) for i in msg.split('\n')]
        joined = "\n".join(mylist)
        splitted = joined.split("\n")
        result = '+-' + '-' * width + '-+'
        for i in splitted:
            if i != "":
                result += '\n| {0:{1}} |'.format(i, width)
        return result + '\n+-' + '-' * width + '-+'


class Stat(PokedexObject):
    def __init__(self, name, _id=None, battle_only=None, base_stat=None):
        """
        Create a Stat object that is used when querying in Expanded Mode.
        :param name: String
        :param _id: int
        :param battle_only: bool
        """
        super().__init__(name, _id)
        self.battle_only = battle_only
        self.base_stat = base_stat

    def __str__(self):

        stri = ""
        if self.battle_only is None:
            stri += "Stat Name: {}\nBase Stat: {}\n".format(self.name, self.base_stat)
        else:
            stri += "Stat Name: {}\nStat ID: {}\nBattle Only: {}\n" \
                   "Base Stat: {}\n".format(self.name, self._id, self.battle_only, self.base_stat)

        return textwrap.indent(text=stri, prefix='+ ', predicate=lambda line: True)
