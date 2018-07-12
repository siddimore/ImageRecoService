from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.callbacks import ModelCheckpoint
from keras.constraints import max_norm


dim = 299
num_training_img = 1190 # number of training images for 17 dataset
num_val_img = 170 # number of validation images for 17 dataset
num_classes = 17 # Change this to 3 (Healthy Lettuece, !Healthy Lettuce, !Lettuce)
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(dim, dim, 3)))

model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())  # go from 3D to 1D
model.add(Dense(64))  # Fully connected layer
model.add(Activation('relu'))
model.add(Dropout(0.5))  # dropout to avoid over-fitting from: https://www.cs.toronto.edu/~hinton/absps/JMLRdropout.pdf
model.add(Dense(17))  # fully connected output layer
model.add(Activation('softmax'))  # softmax the output within the range of (0 to 1) for prediction capabilities


#  This compiles the model architecture and the necessary functions that we
#  categorical crossentropy is the loss function for classification problems with more than 2 classes
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',  # a very nice optimization function with an adaptable learning rate
              metrics=['accuracy']) # want to see how accurate the model is (but are minimize the loss)

batch_size = 16  # a batch size of 16 seemed to be optimal - high accuracy while still being quick

train_datagen = ImageDataGenerator(
        rescale=1./255,  # regularise RGB channels (doesn't affect the actual color)
        zoom_range=[.65, 1],  # we are zooming in at most 35%, so in the range of 0 to 35%
        horizontal_flip=True,  # flipping the image horizontally
        fill_mode='constant')

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        '17_flowers/train',
        target_size=(dim, dim),  # resize train image to dim * dim
        batch_size=batch_size,
        class_mode='categorical')  # class mode is categorical - list with n-classes that points to the class it is

validation_generator = test_datagen.flow_from_directory(
        '17_flowers/validation',
        target_size=(dim, dim),  # resize validation image to dim * dim
        batch_size=batch_size,
        class_mode='categorical')  # class mode is categorical - list with n-classes that points to the class it is

print(validation_generator.class_indices)  # allows us to see where the model will point to each class

# This is the main training of the model itself
# it will run through about 50 epochs of the data (is not used for the 102 class dataset)
# With 50 epochs it begins to over-fit on the training data
# this is due to a low quantity of data that we have available
model.fit_generator(
        train_generator,  # passes the training data through this to transform it
        steps_per_epoch=num_training_img // batch_size,  # how many times we are stepping for each epoch
        epochs=50, 
        validation_data=validation_generator,  # passes the validation data through this
        validation_steps=num_val_img // batch_size,
        callbacks=[ModelCheckpoint('model.h5', verbose=1, save_best_only=True)])  # save model when val_loss decreases

model.summary()  # print out summary of model for testing purposes
