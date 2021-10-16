from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from keras import backend

def prediction():
	backend.clear_session()
	mod=load_model('E:/website/eye/model.hd5')

	test_ob=ImageDataGenerator(rescale=1./255)

	import os
	project_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	img_url=os.path.join(project_path,'test_images')

	

	test_data=test_ob.flow_from_directory(img_url,target_size=(64,64),batch_size=32,class_mode='binary',shuffle=False)
	predicted=mod.predict_generator(test_data)
	y_pred = predicted[0][0] > 0.4

	return y_pred,round(predicted[0][0]*100,2)


if __name__ == '__main__':
    print(prediction())	

