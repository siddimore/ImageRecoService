# Service To Do Basic Image Classification using keras and flask

a. PreTrained Model Used like ResNet50 and InceptionV3
b. Flask Service To Wrap the Model and load it
c. Predict API to give image and get results

# Sample Test
1. Git Clone Repo
2. In Terminal Navigate to where Project is cloned
3. Run Service: python imageclassifierservice.py
4. Open another terminal window
5. curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'

# Result For Lettuce Image:
curl -X POST -F image=@lettuce.jpg 'http://localhost:5000/predict'
{
  "predictions": [
    {
      "label": "head_cabbage", 
      "probablity": 0.9254592657089233
    }, 
    {
      "label": "ice_cream", 
      "probablity": 0.023381194099783897
    }, 
    {
      "label": "buckeye", 
      "probablity": 0.010577011853456497
    }, 
    {
      "label": "cauliflower", 
      "probablity": 0.009751381352543831
    }, 
    {
      "label": "pot", 
      "probablity": 0.006540040019899607
    }
  ], 
  "success": true
}
