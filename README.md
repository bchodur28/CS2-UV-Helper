# CS2-UV-Helper
## Summary
This repository contains a simple Blender addon written in Python that performs three operations (with the possibility of more in the future). These addons include UV Separation, UV Seamless Alignment, and UV Grid Alignment (all of which will be explained in more detail below). NOTE: The UV Seamless Alignment assumes you know the physical size of your texture. This feature is allowed in Substance Printer (I cannot say whether it is allowed in other software, as I only work in Substance Printer for texturing).

## Project Purpose and Motivation
This project started as a very simple method for compacting UVs during asset creation in “Cities Skylines II” (which I will refer to as CS2 going forward), a city-building game that lets you create and share assets. One requirement when UV wrapping your asset is that UVs cannot extend beyond the space. Normally, this UV wrapping is usually fine; going over it will just repeat the texture.

## Understanding the first problem
Imagine you are trying to unwrap a UV texture on an asset that is huge, let's say a building. Here is what you might do.
