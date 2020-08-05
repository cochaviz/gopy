# gopy
> Go game written in python, without any dependecies

It's currently playable with any number of players, and any board size. These options can be edited in the `launcher.py` file.
In the future, the game should be completely independent of the graphics. As it currently stands, however, the `game_manager` has most of the 'graphics' running in there.
If you wanted to use the `go` package to create your own Go (please message me, I would love to see it!), you should create your own or edit the current `game_manager`. Everything should be interfaced from there.

Any different versions of go could be made using the board size, and rulebooks paramaters. The rulebook should be easily extendable to allow for that.
Just create a new rulebook and put that as a paramater in the `Game` object. 
By default, the board size will be set to 19, and the ruleset will be the `Standard` (Korean) Go rules.
