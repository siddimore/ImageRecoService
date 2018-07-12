from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
import numpy as np
from scipy.misc import imresize




#  names is for the 17 classes
names = {'buttercup': 1, 'tigerlily': 14, 'bluebell': 0, 'crocus': 4, 'daisy': 6, 'snowdrop': 12, 'lily_valley': 10,
         'tulip': 15, 'daffodil': 5, 'iris': 9, 'pansy': 11, 'colts_foot': 2, 'fritillary': 8, 'dandelion': 7,
         'cowslip': 3, 'windflower': 16, 'sunflower': 13}


def get_name(names, location):
    """
    Reads in the appropriate dictionary of classes and the location of the class we want
    :param names: dictionary of classes and integer labels
    :param location: integer label of flower
    :return: the name of the flower that lines up with the passes location
    """
    for name in names:
        if names[name] == location:
            return name
    return 'invalid location passed to get_name'

def top_five(percentages, names):
    """
    Create the top 5 predictions for the given flower and convert them into percentages.
    :param percentages: list of percentages that line up with class labels
    :param names: is the dictionary that contains the class names and their integer labels
    :return: a list of the top five percentages as tuples with (percent, name_of_flower)
    """
    five = []
    loc = 0
    for percent in percentages:
        if len(five) > 0:
            for value in five:
                if percent > value[0]:
                    five.remove(value)
                    five.append((percent, get_name(names, loc)))
                    break
                elif len(five) < 5:
                    five.append((percent, get_name(names, loc)))
                    break

        else:
            five.append((percent, get_name(names, loc)))
        loc += 1
    five.sort(key=lambda flow_tup: flow_tup[0], reverse=True)
    return five

def create_percentages(probabilities):
    """
    Take a numpy array containing the probabilities of some other input
    data for what appropriate flower class it belongs to.
    :param probabilities: a numpy array of float values which are probabilities
    :return: a numpy array of float values as percentages
    """
    sum = np.sum(probabilities)
    percentages = []  # standard python list to contain the percentages

    # to calculate the percentage take each independent probability and divide it by the sum of all
    for prob in np.nditer(probabilities):
        percentages.append((prob / sum) * 100)

    return percentages

def format_top_five(five):
    """
    Format the top five predictions into a more pleasing look
    :param five: list of top five percentages containing tuples (percentage, name)
    :return: Formatted string of the predictions
    """
    result = '\n***** Top Five Predictions *****\n\n'
    result += 'Confidence\t\tFlower Name\n'
    result += '==================================\n\n'
    for pair in five:
        result += str(round(pair[0], 2)) + '%' + '\t\t\t' + pair[1] + '\n'
    return result


def init_model(to_load=None, is_17=True):
    """
    Initialize the model to use for predicting
    :param to_load: file name of the model to load
    :param is_17: whether it is the 17 class model or the 102 class model
    :return: a tuple containing the (model, classdict)
    """

    print('Loading model', to_load, '\n\n')
    model = load_model(to_load)

    dict = names


    print('Model loaded successfully.\n')
    return model, dict

def predict(model_tuple):
    """
    Prompts the user for an image to predict.
    Preprocess the image to regularize the RGB colors
            resizes the image to dimensions of (1, dim, dim, 3)
            where 1 is the batch size
                dim is the HxW of the image
                and 3 is how many color channels there are
    :param model_tuple: is a tuple that contains (model, dictionary)
    :return: The top five predictions for the given image
    """
    classes = model_tuple[1]
    model = model_tuple[0]
    dim = 299  # image height and width dimensions
    default_path = 'predict/'
    print('Please enter the full name of the image to predict.\nNote: must be in directory predict/to_predict/\n')
    image_name = input()  # grab user input for the path of image to predict
    if image_name == 'exit':
        exit(0)
    img = load_img(default_path + image_name)
    x = imresize(img_to_array(img), (dim, dim, 3))
    x = x.reshape((1,) + x.shape)  # get the proper # of dimensions - only predict 1 image at a time

    predict_d = ImageDataGenerator(rescale=1. / 255)  # regularize
    # preprocess the image in an infinite loop
    for batch in predict_d.flow(x, batch_size=1):
        x = batch  # this runs in an infinite loop - need to stop it
        break

    prediction = model.predict(x, 1)  # predict what the classes should be

    percentages = create_percentages(prediction)
    print(format_top_five(top_five(percentages, classes)))


model = init_model(to_load='model.h5')

while True:
    predict(model)
# Returns a compiled model identical to the previous one
# loaded_model = load_model('model.h5')
#
# loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
# score = loaded_model.evaluate(X, Y, verbose=0)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
