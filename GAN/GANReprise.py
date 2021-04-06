
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#                              Imports                              #
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
import cv2
import keras
import os
import numpy as np
from tqdm import tqdm
from glob import glob
from tensorflow.keras.optimizers import Adam
from keras.models import Sequential, load_model
from keras.layers import Conv2D, Dense, MaxPooling2D, Flatten, Reshape, UpSampling2D
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#                CHARGER + PREPARER IMAGE REELLES DATA              #
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

optimizer = Adam(lr=0.0002, beta_1=0.5)

images_vraies =[]

noms_image = glob("dataSet/*")

for nom in tqdm(noms_image):
	image = cv2.imread(nom, cv2.IMREAD_COLOR)
	image = cv2.resize(image, (256,256))
	image = image.astype("float32")	
	image = (image-127.5)/127.5
	images_vraies.append(image)

images_vraies = np.array(images_vraies)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#                        Charger Discriminateur                     #
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
discriminateur = load_model("Discriminateurs/discriminateur_epoch5500.h5")
discriminateur.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
print("Discriminateur Chargé")
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#                        Charger Générateur                         #
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
generateur = load_model("Generateurs/generateur_epoch5500.h5")
print("Generateur Chargé")
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#                          Créer COMBO                              #
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
combo = Sequential()
combo.add(generateur)
combo.add(discriminateur)

discriminateur.trainable = False
combo.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

print("COMBO :")
combo.summary()
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
#                           Entrainer                               #
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
iterations = 40000
demi_batch= 16

for iteration in range(iterations):
	os.system('cls' if os.name == 'nt' else 'clear')
	print()
	print(" ##################################")
	print("   Boucle n°"+str(iteration)+"/"+str(iterations))
	print(" ##################################")
	################################################
	# créer pack de données pour le discriminateur #
	################################################
	# etape 1 : prendre des bonnes images
	# etape 2 : créer les labels (1 pour vrai) pour les bonnes images du dataset
	# etape 3 : generer des mauvaises images
	# etape 4 : créer les labels (0 pour faux) pour les mauvaises images générés

	x = []
	y = []

	# etape 1 : prendre des bonnes images
	images_bonnes = images_vraies[np.random.randint(0, images_vraies.shape[0], size=demi_batch)]
	# etape 2 : créer les labels (1 pour vrai) pour les bonnes images du dataset
	labels_bonnes = np.ones(demi_batch) #un tableau avec 1000 fois le label 1
	# etape 3 : generer des mauvaises images
	bruit = np.random.normal(0, 1, size=[demi_batch,100]) # 1000 tableaux de 100 nombres aléatoires
	images_mauvaises = generateur.predict(bruit) # milles images générées
	# etape 4 : créer les labels (0 pour faux) pour les mauvaises images générés
	labels_mauvaises = np.zeros(demi_batch)

	x = np.concatenate([images_bonnes,images_mauvaises])
	y = np.concatenate([labels_bonnes,labels_mauvaises])

	############################
	# entrainer discriminateur #
	############################
	discriminateur.trainable = True
	print()
	print("Entrainement du discriminateur :")
	print()
	discriminateur.fit(x,y, epochs = 1, batch_size=32)


	#######################################
	# créer pack de données pour le combo #
	#######################################
	# generer du bruit
	bruit = np.random.normal(0, 1, size=[demi_batch,100]) # 1000 tableaux de 100 nombres aléatoires
	# créer les labels 1
	labels_combo = np.ones(demi_batch)


	###################
	# entrainer combo #
	###################
	print()
	print("Entrainement du Générateur :")
	print()
	discriminateur.trainable = False
	combo.fit(bruit,labels_combo, epochs=1, batch_size=32)

	################################################################
	# toutes les 5 itérations générer 1 images et la sauvegarder   #
	################################################################
	if iteration % 25 == 0 :
		bruit = np.random.normal(0, 1, size=[1, 100])
		print("Génération d'image...")
		print()
		image = generateur.predict(bruit)
		image = (image*127.5)+127.5
		image = image.astype("uint8")
		image = image.reshape((256,256,3))
		imname = "genim_"+str(iteration)+".jpg"
		cv2.imwrite("Images_reprise/" +imname, image)
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
	#                      Sauvegarder Les Models                       #
	#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
	if iteration % 500 == 0 and iteration != 0 :
		print()
		print("Sauvegarde des models...")
		print()
		discriminateur.save("Discriminateurs/discriminateur_REPRISE_epoch"+str(iteration)+".h5")
		generateur.save("Generateurs/generateur_REPRISE_epoch"+str(iteration)+".h5")
