import abc


class PokedexObject(abc.ABC):
    def __init__(self, name, _id):
        self.name = name
        self.id = _id


class Pokemon(PokedexObject):
    pass


class Ability(PokedexObject):
    pass


class Move(PokedexObject):
    pass


class Stat(PokedexObject):
    pass



