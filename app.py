from keras.applications import InceptionV3,ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
from yoloimage import yoloImageCrop
import numpy as np
import flask
import io


# Initialize Flask application
app = flask.Flask(__name__)
model = None


def load_model():
    # Load Pretrained Model
    global model
    # model = InceptionV3(weights = "imagenet")
    model = ResNet50(weights = "imagenet")
    print(model.summary())


def prepare_image(image, target):
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize input image and preprocess
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)
    image = yoloImageCrop(image)
    
    return image

@app.route('/')
def homepage():
    load_model()
    return """Welcome To LettuceRecoService"""


@app.route("/predict", methods=["POST"])
def predict():

    # Init the data dictionaru that will be returned to the view
    data = {"success": False}

    if flask.request.method == "POST":
        if flask.request.files.get("image"):

            # Read image
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))

            image = prepare_image(image, target=(224,224))

            # classify image and init list of predictions to return
            preds = model.predict(image)
            results = imagenet_utils.decode_predictions(preds)

            data["predictions"] = []

            # Loop over results
            for(imagenetID, label, prob) in results[0]:
                r = {"label":label, "probablity":float(prob)}
                data["predictions"].append(r)

            data["success"] = True

    return flask.jsonify(data)



# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    load_model()
    app.run()
