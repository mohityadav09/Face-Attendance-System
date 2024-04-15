import pandas as pd 
import numpy as np 
import cv2

class imageData:
    def __init__(self):
        self.images=[]
        self.labels=[]
        data = pd.read_csv("images_details.csv")
        folder_path = "images"
        for i in range(len(data)):
            self.images.append(f"{folder_path}/{data['image'][i]}")
            self.labels.append(data["id"][i])
    def length(self):
        return len(self.images)

    def transform(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            return None
        #image=cv2.resize(image,(216,216))
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return rgb_image

    def get_image(self, index):
        image_path = self.images[index]
        transformed_image = self.transform(image_path)
        if transformed_image is None:
            print(f"Failed to read image: {image_path}")
            return None, None
        label = self.labels[index]
        return transformed_image, label

image_data = imageData()
img, label = image_data.get_image(0)
if img is not None:
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
print(label)
