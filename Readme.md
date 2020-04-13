# COMP 3522 Assignment 3: Pokedex
This program allows users to query against the [PokeAPI](https://pokeapi.co/). The program will return the 
output in the terminal console, or save the output to a given text file.  

## Installation
Please have Python3 installed.
Users should not have to install external libraries for the program to run. 

## Usage
To run the program, users must enter input in the command line. Here is the format:

`python3 pokedex.py {"pokemon" | "ability" | "move"} {--inputfile "filename.txt" | --inputdata "name or id" } 
[--expanded] [--output "outputfile.txt"]`

NOTE: `python3` may not be a recognized command for some. Use `python` instead. 

### Mode
The program will return results for Pokemons, abilities, or moves. Please specify which one in the terminal input using
`"pokemon"`, `"ability"`, or `"move"`.

### Input
The program can query a single input or multiple inputs. Multiple inputs must be in a text file. 
Queries can be made using an ID (integer) or name.

### Expanded
Only the Pokemon queries can be expanded at this moment. Stats, Abilities, and Moves of a Pokemon will be expanded to return
more details if indicated. This parameter is optional. 

### Output
This parameter is optional. If output is not specified, the results will be printed to the console. If an output
file is specified, the results will be saved to that file.

### Results
Here are some sample results for a Pokemon (expanded and not expanded), Ability, and Move:

Expanded Pokemon:
```
+----------------------------------------------------------------------------------+
|                                 Pokemon Details                                  |
+----------------------------------------------------------------------------------+
| + Pokemon Name:   ditto                                                          |
| + Pokedex ID:     132                                                            |
| + Height:         3 decimetres                                                   |
| + Weight:         40 hectograms                                                  |
| + Types:          normal                                                         |
+----------------------------------------------------------------------------------+
|                                      Stats                                       |
+----------------------------------------------------------------------------------+
| + Stat Name: speed                                                               |
| + Stat ID: 6                                                                     |
| + Battle Only: False                                                             |
| + Base Stat: 48                                                                  |
| -------------------------------------------------------------------------------- |
| + Stat Name: special-defense                                                     |
| + Stat ID: 5                                                                     |
| + Battle Only: False                                                             |
| + Base Stat: 48                                                                  |
| -------------------------------------------------------------------------------- |
| + Stat Name: special-attack                                                      |
| + Stat ID: 4                                                                     |
| + Battle Only: False                                                             |
| + Base Stat: 48                                                                  |
| -------------------------------------------------------------------------------- |
| + Stat Name: defense                                                             |
| + Stat ID: 3                                                                     |
| + Battle Only: False                                                             |
| + Base Stat: 48                                                                  |
| -------------------------------------------------------------------------------- |
| + Stat Name: attack                                                              |
| + Stat ID: 2                                                                     |
| + Battle Only: False                                                             |
| + Base Stat: 48                                                                  |
| -------------------------------------------------------------------------------- |
| + Stat Name: hp                                                                  |
| + Stat ID: 1                                                                     |
| + Battle Only: False                                                             |
| + Base Stat: 48                                                                  |
| -------------------------------------------------------------------------------- |
+----------------------------------------------------------------------------------+
|                                    Abilities                                     |
+----------------------------------------------------------------------------------+
| + Ability Name: imposter                                                         |
| + Ability ID: 150                                                                |
| + Generation: generation-v                                                       |
| + Effect: This Pok�mon transforms into a random opponent upon entering battle.   |
| This effect is identical to the move transform.                                  |
| + Short Effect: Transforms upon entering battle.                                 |
| + Pokemons with same ability: ['ditto']                                          |
+----------------------------------------------------------------------------------+
+----------------------------------------------------------------------------------+
| + Ability Name: limber                                                           |
| + Ability ID: 7                                                                  |
| + Generation: generation-iii                                                     |
| + Effect: This Pok�mon cannot be paralyzed.                                      |
| +                                                                                |
| + If a Pok�mon is paralyzed and acquires this ability, its paralysis is healed;  |
| this includes when regaining a lost ability upon leaving battle.                 |
| + Short Effect: Prevents paralysis.                                              |
| + Pokemons with same ability: ['persian', 'hitmonlee', 'ditto', 'buneary',       |
| 'lopunny', 'glameow', 'purrloin', 'liepard', 'stunfisk', 'hawlucha', 'mareanie', |
| 'toxapex']                                                                       |
+----------------------------------------------------------------------------------+
+----------------------------------------------------------------------------------+
|                                      Moves                                       |
+----------------------------------------------------------------------------------+
| + Move Name: transform                                                           |
| + Move ID: 144                                                                   |
| + Generation: generation-i                                                       |
| + Accuracy: None                                                                 |
| + PP: 10                                                                         |
| + Power: None                                                                    |
| + Type: normal                                                                   |
| + Damage Class: status                                                           |
| + Effect: User becomes a copy of the target until it leaves battle.              |
+----------------------------------------------------------------------------------+
```

Non-expanded Pokemon:
```
+----------------------------------------------------------------------------------+
|                                 Pokemon Details                                  |
+----------------------------------------------------------------------------------+
| + Pokemon Name:   ditto                                                          |
| + Pokedex ID:     132                                                            |
| + Height:         3 decimetres                                                   |
| + Weight:         40 hectograms                                                  |
| + Types:          normal                                                         |
+----------------------------------------------------------------------------------+
|                                      Stats                                       |
+----------------------------------------------------------------------------------+
| + Stat Name: speed                                                               |
| + Base Stat: 48                                                                  |
| -------------------------------------------------------------------------------- |
| + Stat Name: special-defense                                                     |
| + Base Stat: 48                                                                  |
| -------------------------------------------------------------------------------- |
| + Stat Name: special-attack                                                      |
| + Base Stat: 48                                                                  |
| -------------------------------------------------------------------------------- |
| + Stat Name: defense                                                             |
| + Base Stat: 48                                                                  |
| -------------------------------------------------------------------------------- |
| + Stat Name: attack                                                              |
| + Base Stat: 48                                                                  |
| -------------------------------------------------------------------------------- |
| + Stat Name: hp                                                                  |
| + Base Stat: 48                                                                  |
| -------------------------------------------------------------------------------- |
+----------------------------------------------------------------------------------+
|                                    Abilities                                     |
+----------------------------------------------------------------------------------+
| + Ability Name: imposter                                                         |
+----------------------------------------------------------------------------------+
+----------------------------------------------------------------------------------+
| + Ability Name: limber                                                           |
+----------------------------------------------------------------------------------+
+----------------------------------------------------------------------------------+
|                                      Moves                                       |
+----------------------------------------------------------------------------------+
| + Move Name: transform                                                           |
| + Level Acquired: 1                                                              |
+----------------------------------------------------------------------------------+
```

Ability:
```
+----------------------------------------------------------------------------------+
| + Ability Name: stench                                                           |
| + Ability ID: 1                                                                  |
| + Generation: generation-iii                                                     |
| + Effect: This Pokémon's damaging moves have a 10% chance to make the target     |
| flinch with each hit if they do not already cause flinching as a secondary       |
| effect.                                                                          |
| +                                                                                |
| + This ability does not stack with a held item.                                  |
| +                                                                                |
| + Overworld: The wild encounter rate is halved while this Pokémon is first in    |
| the party.                                                                       |
| + Short Effect: Has a 10% chance of making target Pokémon flinch with each hit.  |
| + Pokemons with same ability: ['gloom', 'grimer', 'muk', 'stunky', 'skuntank',   |
| 'trubbish', 'garbodor']                                                          |
+----------------------------------------------------------------------------------+
```

Move:
```
+----------------------------------------------------------------------------------+
| + Move Name: pound                                                               |
| + Move ID: 1                                                                     |
| + Generation: generation-i                                                       |
| + Accuracy: 100                                                                  |
| + PP: 35                                                                         |
| + Power: 40                                                                      |
| + Type: normal                                                                   |
| + Damage Class: physical                                                         |
| + Effect: Inflicts regular damage with no additional effect.                     |
+----------------------------------------------------------------------------------+
```

## Contributors
Authors: 
* Kihyun Choi, A01005378, Set 3V
* Vicky Chung, A01054885, Set 3M
