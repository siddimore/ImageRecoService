#Service To Do Basic Image Classification using keras and flask

a. PreTrained Model Used like ResNet50 and InceptionV3
b. Flask Service To Wrap the Model and load it
c. Predict API to give image and get results

#Sample Test
1. Git Clone Repo
2. In Terminal Navigate to where Project is cloned
3. Run Service: python imageclassifierservice.py
4. Open another terminal window
5. curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'

Result For Dog Image:
{
  "predictions": [
    {
      "label": "beagle",
      "probablity": 0.9830568432807922
    },
    {
      "label": "pot",
      "probablity": 0.004184032324701548
    },
    {
      "label": "Walker_hound",
      "probablity": 0.0036015023943036795
    },
    {
      "label": "bluetick",
      "probablity": 0.0016072390135377645
    },
    {
      "label": "Brittany_spaniel",
      "probablity": 0.0010771512752398849
    }
  ],
  "success": true
}
