# mirror-mult-obj-bpy
My first Blender addon, an addon that makes symmetry and mirroring among multiple objects way less tedious!

# :notebook_with_decorative_cover: Description
This addon contains **2** panels, one for mirroring multiple objects along 1 or more of the 3 orthogonal axes[^1], named ***MirrorMult***, and another one for rotational symmetry which is just referred to as ***RotSymm***, for shorthand. 

I made this addon since I felt that symmetrical designs were just way too tedious to make procedurally within Blender. To do it, you had to add an individual *Mirror* modifier to each object, select its *Mirror Object*, and then select the axes over which it would be reflected. That's just... way too much work... especially for objects with a bunch of other modifiers, meaning you can't just use ***Copy Modifiers*** and call it a day[^2]. 

So, I just spent a good couple hours of my time to make this addon!

# :book: History
Back a year or two ago, I made a very simple version of the addon that just consisted of the ***MirrorMult*** panel. I was just getting into programming and I followed step-by-step guides on how BPy[^3] works and some of the fundamentals like syntax and file organization. I've learnt a lot more about Blender at this point, and so I needed a better addon that could help more with these symmetrical, almost futuristic designs that I've been wanting to make. 

In Blender, rotational symmetry doesn't actually exist. It's done through a sort of "hack" where you use the **Array** modifier and use a rotated object as its Object Offset. Doing this for so many objects, and having to manually rotate the central object a certain amount depending on how many copies you wanted around the origin was just annoying. So, I decided to update my old addon with a cooler UI and more organizational features, which you'll see in the later sections! 

As I hadn't touched the BPy API in so long, it took a lot of time to get readjusted to the way it worked[^4]. This was really frustrating and honestly caused me to lose a lot of faith in myself and my coding competency. However, I simply took this as motivation to keep going forward, as letting this feeling overtake me would just mean I would get consistently worse. Over time, I started getting a better understanding of the syntax and how everything works, and before I knew it, I was working efficiently and understanding everything I was doing. You can see from the number of comments in the Python file how dedicated I was to making sure I wouldn't forget any of these details. With the addon finally finished (and after an embarrassing amount of debugging and refactoring), I'm very happy with the final product and I'll be using this addon for so many of my projects!

(p.s. maybe I'll keep adding more features to this addon as time goes by, I want this addon to just hold a bunch of features that make difficult designs easier!)

Anyway, enough about me, here's how the addon works!

# :last_quarter_moon: MirrorMult
This panel allows you to reflect your selected objects over the active object, over whatever axes you want!

## Features:
* Multi-axis mirroring
* Parenting objects to the reflection object, to make positioning and organization easier!
* Undo button[^5]

Using this panel just goes as follows:
1. Select all of the objects you want reflected
2. Select the object that you want to use as the point of reflection
   + Make sure that this "reflector object" is selected last, so that it becomes the ***Active Object*** and has a lighter orange outline
3. In the panel, select the axes that you want the objects to be reflected over
4. Press the `Mirror Selected Objects` button and enjoy your symmetrical design!

https://user-images.githubusercontent.com/121361927/236517415-6182d157-2d91-46bc-a523-a3570947c7f5.mov

# :low_brightness: RotSymm
This panel allows for easy rotational symmetry, by rotating selected objects around a certain origin point and around a certain axis! 

## Features:
* Control how many copies you want around the rotation
* Select either the 3D Cursor or the Active Object as your origin points
* Rotational symmetry around any one of the orthogonal axes[^1]

Here's how to use this panel:
1. Select all the objects you want to have in the rotational symmetry

The next step depends on what you want the origin to be. __If you want the `3D Cursor` to be your origin point, then skip step 2__. However, if you want the origin point to be the `Active Object Origin`, then:

2. Select the object whose origin you want to be the origin point, and in the panel, make sure to select `Active Obj. Origin` in the dropdown menu

3. Use the slider to choose how many copies of the selected objects you want in the symmetry
4. Select the rotational axis from the X, Y, and Z buttons
5. Then, just hit `Rotationally Symmetrize` and enjoy your beautiful mandala-like pattern!

https://user-images.githubusercontent.com/121361927/236517428-f574fb11-c124-4966-8875-fcc6d602c19d.mov

[^1]: You know, the X, Y, and Z axes
[^2]: Blender actually has a feature in the Graph Editor menu that allows you to copy a certain group of modifiers to another property on the Editor itself. I feel like this should be a thing for objects as well, not just for the Graph Editor?? IDK, since it doesn't exist, my addon will have to do!
[^3]: Blender's Python API
[^4]: One thing that was unnecessarily hard to understand was the fact that creating a variable to hold something like the 3D Cursor's location doesn't actually hold the cursor's location at that instant, but that variable is actually just a reference to the 3D Cursor's location, and so the variable changes as one moves the 3D Cursor around. This was so annoying as I referred to things like the Active Object using this syntax, and I would get so confused when I saw that the object I had in a variable was always changing :sob:
[^5]: Honestly, I don't really see the purpose of the undo button anymore since CMD+Z exists but it just worked as a way for me to practice using lambda functions, so I'll keep it for the memories :). 
