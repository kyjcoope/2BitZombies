Test Engine:
Run, gameDemo.py to test gameEngine

player:
	use left and right key to move left and right
	use space bar to shoot
	use up key to jump

enemy:
	spawns at random x location after being shot by player



gameEngine details:
   gameEngine.py uses pygame in limited capacity to make a window and place an image on that window.
   gameDemo uses pygame for key presses.
   All sprite and scene classes are created in the gameEngine and do not use pygame.
   Collisions are done inside the gameEngine and do not use pygame.
   Image scaling, rotation, and flipping are doing using pygame.transform
   
   gameEngine has two main classes, Scene and Sprite.
   
   Scene, only takes one argument a tuple for resolution: (x, y)
      Scene, does all setup of pygame automatically
      set scene.backgroundColor to color you want the background

   Sprite, takes 5 arguments: 
(scene, x_loc, y_loc, img, classtype)
      
   scene, is the scene the spring belongs to, multiple scenes can be made to easily,
   swap between environments.

   x_loc, y_loc, is where the sprite will be placed on screen.

   img, is the image that the sprite will use

   classtype, lets you classify your sprite, this is used for collisions

   