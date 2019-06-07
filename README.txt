///////////////////////////////////////////////////////////////////////////////////////////////
/// Game: 2BitZombies
/// Engine: gameEngine/pygame (not andy harris gameEngine)
/// Data: 12/4/2018
///////////////////////////////////////////////////////////////////////////////////////////////

Introduction:
	2BitZombies is a 2d platformer, where the player must survive
as zombies continuously attack them in a never ending swarm. The only
way to go is up...

Goal:
	To reach the magic gold coin at the top center of the map by building
your way there.

Controls:
	W == jump
	A == move left
	D == move right
	S == drop down a level
	1 == build tool
	2 == weapon
	LMC == build/shoot
	P == hardreset button

Player:
	The player HUD is in the top left corner of the game window.
It shows how many hearts the player currently has, as well as how many
boxes the player has/can place. It also shows which weapon/tool the player
currently has selected.

Tools/weapons:
	The player has two tools at his disposal a block building tool
and a weapon to kill zombies with.

Note: the building tool with only build a box if the box either on
the ground or has another box under it or beside it.

Zombies:
	Zombies will attack either you or the base of your structure.
If a zombie destroys a box and your structure does't have away to ground
anymore, your structure will selfdestruct. If a zombie dies it will either
drop a heart or a box that you can pickup. Zombies will spawn off screen
then walk on screen.






***************************************************************************
***************************************************************************
*** PROGRAM OVERVIEW
***************************************************************************
***************************************************************************

main() gets, called at the start up.

main() contains all declarations/initiations, and the main game loop.

When the game is restarted current game quits and main is called again.

The main game loop, updates sprites, checks win conditions, spawns enemys,
and builds HUD.

Level, is built from a tile map which is a 2d list in world.py

A copy of this world list is made and any box that is made has its location noted
in the list.

Boxes can easily check if other boxes are next to them, by checking
the 2d list. Since every box is 20px by 20px we can use,
int(positionX/20) and int(positionY/20) to get the row and column information for the
list and check its neighbours

This can also be used to easily check if a sprite is about to fall
through the ground. By getting column and row information similarly to
int(positionX/20) and int(positionY/20), we can look downwards.

int(positionY+dy)/20 will give which box the sprite would
have be inside. dy can then be updated to be the top of the box
so it gets placed on top of the box and not inside it. 