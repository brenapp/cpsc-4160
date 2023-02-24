# Pybox

<img width="1392" alt="Screenshot 2023-02-24 at 10 55 28 AM" src="https://user-images.githubusercontent.com/8839926/221226235-dcaea19d-d9e0-4431-b7b7-f6659ee9478a.png">

> Python: 3.10.7
> Pygame Version: 2.1.2
> OS: OS X Ventura 13.1

This is a resurrection/re-implementation of one of the first projects I made when I was learning web
development, called [boxgame](https://github.com/MayorMonty/boxgame). boxgame was centered around
moving an agent (a box). Obviously, I have skilled up a lot as a developer since then, so a lot of 
the focus of this project was on creating a modular and reusable design for code

The user can move the box by pressing the left and right arrow keys, and press the up arrow to shoot a laser at enemies. However, be careful as the lasers don't go away until they hit something, including you!

# Description of Implementation

![image](https://user-images.githubusercontent.com/8839926/221232555-9e54d367-2a5b-4968-86ca-60a0790df27c.png)

All of the entities in Boxgame are based off a singular Entity class that contains all of the elements of MVC for a single entity. The Entity allows subclasses to store state (model), update that state periodically bassed on user input (controller), and define their own render functions (view). Different types of Entities subclass the Entity abstract class and can define their own `render()`, `update_state()` and `handle_event()` functions to define different aspects of the entity lifecycle. In addition, Entity provides a number of utility methods for accessing entities, and removing entities from the global list.

# Future Work

The structure of the Entity system allows us to easily create additional types of entities, as long as we define the lifecycle methods that can handle them. By defining different types of entities, we can create entirely new games from this structure.

Right now, there is not a good structure for code that occurs between multiple enties, like handling collisisons. In future projects, I would like to expand my codebase to include elements of a Entity Component System model to properly handle more abstract interactions between entities that aren't fully within a single element.
