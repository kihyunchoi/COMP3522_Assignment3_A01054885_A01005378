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
        width = 86
        stats = ""
        for s in self.stats:
            stats += "\n" + s.__str__() + "-" * width

        moves = ""
        for m in self.moves:
            moves += "\n" + m.__str__() + "-" * width

        abilities = ""
        for a in self.abilities:
            abilities += "\n" + a.__str__() + "-" * width



        str = "Pokemon Name: {:>10}\nPokedex ID: {:>10}" \
              "\nHeight: {:>10} decimetres\nWeight: {:>10} hectograms" \
              "\nTypes: {}\n".format(self.name, self.get_id(), self.height, self.weight, self.types)

        # Formatting Stats
        str += '+-' + '-' * width + '-+'
        str += '\n| {0:^{1}} |'.format("Stats", width)
        str += '\n+-' + '-' * width + '-+'

        wrapper = textwrap.TextWrapper(width=width)
        mylist = [wrapper.wrap(i) for i in stats.split('\n') if i != '']
        for i in mylist:
            str += '\n| {0:{1}} |'.format(i[0], width)

        str += '\n+-' + '-' * (width) + '-+'

        # Formatting Abilities
        width = 86
        str += '\n+-' + '-' * width + '-+'
        str += '\n| {0:^{1}} |'.format("Abilities", width)
        str += '\n+-' + '-' * width + '-+'
        mylist = [textwrap.fill(i, width=width) for i in abilities.split('\n')]
        joined = "\n".join(mylist)
        splitted = joined.split("\n")
        for i in splitted:
            if i != "":
                str += '\n| {0:{1}} |'.format(i, width)
        str += '\n+-' + '-' * (width) + '-+'

        # Formatting Moves
        str += "\n" + "-" * 30 + "\n\tMoves\n" + "-" * 30 + "\n{}".format(moves)

        return str


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
        str = ""
        if self._id is None:
            str += "Ability Name: {}\n".format(self.name)
        else:
            str += "Ability Name: {}\nAbility ID: {}\nGeneration: {}\nEffect: {}\nShort Effect: {}\n" \
                   "Pokemons with same ability: {}\n".format(self.name, self._id, self.generation, self.effect,
                                                             self.effect_short, self.pokemon)
        return textwrap.indent(text=str, prefix='+ ', predicate=lambda line: True)


class Move(PokedexObject):
    def __init__(self, name, _id=None, generation=None, accuracy=None, pp=None,
                 power=None, type=None, damage_class=None, effect_short=None, level=None):
        """
        Create a Move object.
        :param name: String
        :param _id: int
        :param generation: String
        :param accuracy: int
        :param pp: int
        :param power: int
        :param type: String
        :param damage_class: String
        :param effect_short: String
        """
        super().__init__(name, _id)
        self.generation = generation
        self.accuracy = accuracy
        self.pp = pp
        self.power = power
        self.type = type
        self.damage_class = damage_class
        self.effect_short = effect_short
        self.level = level

    def __str__(self):
        str = ""
        if self.type is None:
            str += "Move Name: {}\nLevel Acquired: {}\n".format(self.name, self.level)
        else:
            str += "Move Name: {}\nMove ID: {}\nGeneration: {}\nAccuracy: {}\nPP: {}\nPower: {}\nType: {}\n" \
                   "Damage Class: {}\nEffect: {}\n".format(self.name, self._id, self.generation, self.accuracy,
                                                           self.pp, self.power, self.type, self.damage_class,
                                                           self.effect_short)
        return str


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
        str = ""
        if self.battle_only is None:
            str += "Stat Name: {}\nBase Stat: {}\n".format(self.name, self.base_stat)
        else:
            str += "Stat Name: {}\nStat ID: {}\nBattle Only: {}\n".format(self.name, self._id, self.battle_only)

        return textwrap.indent(text=str, prefix='+ ', predicate=lambda line: True)
