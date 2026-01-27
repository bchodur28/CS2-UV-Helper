# CS2-UV-Helper
## Summary
This repository contains a simple Blender addon written in Python that performs three operations (with the possibility of more in the future). These addons include UV Separation, UV Seamless Alignment, and UV Grid Alignment (all of which will be explained in more detail below). NOTE: The UV Seamless Alignment assumes you know the physical size of your texture. This feature is allowed in Substance Printer (I cannot say whether it is allowed in other software, as I only work in Substance Printer for texturing).

## Project Purpose and Motivation
This project started as a very simple method for compacting UVs during asset creation in “Cities Skylines II” (which I will refer to as CS2 going forward), a city-building game that lets you create and share assets. One requirement when UV wrapping your asset is that UVs cannot extend beyond the space. Normally, this UV wrapping is usually fine; going over it will just repeat the texture.

### Understanding the point and purpose of this specific addon
Imagine you are trying to unwrap a UV texture on an asset that is huge, let's say a building. Here is what you might do.

<img src="images/first-uv-attempt.png" alt="Alt text" height="400"/>
<img src="images/first-uv-attempt-3d-view.png" alt="Alt text" height="400"/>

Another option we could go with is to collapse all UVs so they overlap. This looks like this.

<img src="images/second-uv-attempt.png" alt="Alt text" height="400"/>
<img src="images/second-uv-attempt-3d-view.png" alt="Alt text" height="400"/>

Here we unwrap the UVs, and for my personal use, I have also set the pixel density to be 2.56 px/cm (You do not need to know the pixel density; it is calculated internally to determine proper alignment). Now this texture is a 4k image that repeats every 2 meters by 2 meters. With a texture density of 2.56 px/cm, this means that if we keep the majority of our assets at that texture density, we have 16 meters by 16 meters of space. However, as we can see, the UVs are simply too large; they extend beyond the space (not allowed in CS2), and lowering the texture density will result in a blurrier texture.

### Alignment Solution

<img src="images/third-uv-attempt.png" alt="Alt text" height="400"/>
<img src="images/third-uv-attempt-3d-view.png" alt="Alt text" height="400"/>

This is where the alignment solution comes in. In the image above, we can see something similar to the second attempt: UVs are overlapped; however, in the 3D view, you see no seams. This is because UV Seamless Alignment aligns the UV to minimize seams. NOTE: I originally made this software for myself with the attitude of good-enoughism (yes, I’m aware that enoughism isn’t a word). This means the program has limitations and cannot eliminate all seams in all situations.
