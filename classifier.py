# A convolutional neural network model (convnet)
# Inspired by @fchollet's http://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html

from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

from PIL import Image
import numpy as np
import os, sys


# Build a model with 3 convolution layers, ReLu activation,
# followed by max-pooling layers.
model = Sequential()
model.add(Convolution2D(32, 3, 3, input_shape=(3, 150, 150)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Then we stack on 2 fully-connected layers
model.add(Flatten()) # converts the 3D feature maps to 1D feature vectors
model.add(Dense(64))
model.add(Activation('relu'))

model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])


if os.path.exists("first_try.h5"):
    model.load_weights('first_try.h5')  # always save your weights after training or during training
else:
    # Randomly augment input images using this generator:
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)
    test_datagen = ImageDataGenerator(rescale=1./255)
    train_generator = train_datagen.flow_from_directory(
        'data/train',  # this is the target directory
        target_size=(150, 150),  # all images will be resized to 150x150
        batch_size=32,
        class_mode='binary')  # since we use binary_crossentropy loss, we need binary labels
    # this is a similar generator, for validation data
    validation_generator = test_datagen.flow_from_directory(
        'data/validation',
        target_size=(150, 150),
        batch_size=32,
        class_mode='binary')
    model.fit_generator(train_generator, samples_per_epoch=2000,
            nb_epoch=50, validation_data=validation_generator,
            nb_val_samples=800)
    model.save_weights('first_try.h5')  # always save your weights after training or during training

def image_to_x(image_path):
    img = Image.open(image_path)
    img.load()
    img = img.resize((150,150))
    data = np.asarray(img, dtype='int32').reshape((1,3,150,150))
    return data

def usage():
    print "Usage:\n\tpython ./classifier.py path_to_image.jpg"

if len(sys.argv) > 1:
    filename = sys.argv[1]
    if os.path.exists(filename):
        x = image_to_x(filename)
        prediction = model.predict(x)[0][0]
        print(prediction)
    else:
        print("File %s does not exist" % filename)
else:
    usage()

