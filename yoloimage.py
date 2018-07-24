from pydarknet import Detector, Image
import cv2
import os

def yoloImageCrop(filepath):
	keywords = ["pottedplant","vase"]
	image = {}
	if ".jpg" in name:
				try:
					img = cv2.imread(filepath)

					img2 = Image(img)

					# r = net.classify(img2)
					results = net.detect(img2)
					

					for cat, score, bounds in results:
						if str(cat.decode("utf-8")) in keywords:
							x, y, w, h = bounds
							print (x,y,w,h)
							#cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
							#cv2.putText(img,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
							im = img[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2)]
							
							image[str(cat.decode("utf-8"))] = im
						#return str(cat.decode("utf-8")), im
						#cv2.imwrite("../labeledimage/"+str(cat.decode("utf-8"))+"_"+name,im)

					# cv2.imshow("output", img)
					# img2 = pydarknet.load_image(img)

					cv2.waitKey(0)
				except:
					print ("FAIL"+name)
	return image

if __name__ == "__main__":
	# net = Detector(bytes("cfg/densenet201.cfg", encoding="utf-8"), bytes("densenet201.weights", encoding="utf-8"), 0, bytes("cfg/imagenet1k.data",encoding="utf-8"))

	net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0, bytes("cfg/coco.data",encoding="utf-8")) # you need this to load the model
	for dirpath, dirs, files in os.walk("/mnt/c/Users/yilzhan/Documents/Good/"):
		for name in files:
			image = yoloImageCrop(dirpath+"/"+name)
			for label in image.keys():
				data = image[label]
				print ("save " + name + " as " + label)
				cv2.imwrite("../labeledimage/"+label+"_"+name,data)
				
			