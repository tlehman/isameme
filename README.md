# Detecting memes using deep convolutional neural networks 

An experiment with [Keras](http://keras.io). 


We will be using MemeGenerator's API to get a collection of popular memes 
and their underlying images. MemeGenerator.net makes this very easy, their 
API gives a JSON response where the `imageUrl` is the underlying image, and 
the `instanceImageUrl` is the meme version of the same image. 

## `imageUrl: https://cdn.meme.am/images/400x/7679243.jpg`

![lomberg](https://cdn.meme.am/images/400x/7679243.jpg)

## `instanceImageUrl: https://cdn.meme.am/instances/400x/69239531.jpg`

![lomberg-meme](https://cdn.meme.am/instances/400x/69239531.jpg)

