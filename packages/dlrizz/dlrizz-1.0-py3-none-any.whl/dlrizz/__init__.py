def index():
    print(""" 

Pip Install:
!pip install numpy
!pip install pandas
!pip install tensorflow
!pip install keras
!pip install scikit-learn 
!pip install scikeras
!pip install matplotlib          
          

Practical 1:
1) Performing matrix multiplication and finding eigen vectors and eigen values using TensorFlow.

Practical 2:
2) Solving XOR problem using deep feed forward |network.
          
Practical 3:
3) Implementing deep neural network for performing binary classification task.

Practical 4:
4a) Using deep feed forward network with Two Hidden layers for performing Multiclass Classification and predicting the class. 
4b) Using a deep feed forward network with two hidden layers for performing classification and predicting the probability of class.
4c) Using a deep feed forward network with two hidden layers for performing linear regression and predicting values.          
         
Practical 5: 
5a) Evaluating feed forward deep network for regression using KFold cross validation. 
5b) Evaluating feed forward deep network for multiclass Classification using KFold crossvalidation. 
          
Practical 6:
6a) Implementing regularization to avoid overfitting in binary classification 
6b) Implement L2 regularization with alpha=0.001 
6c) Replace L2 regularization with L1 regularization.

Practical 7:
7) Demonstrate recurrent neural network that learns to perform sequence analysis for stock price 
          
Practical 8:          
8) Performing encoding and decoding of images using 8 deep autoencoder. 

Practical 9:          
9) Implementation of convolutional neural network to predict numbers from number images. 

Practical 10:         
10) Denoising of images using autoencoder.       
             
""")
    

def prog(num):
    if num =="1":
        print(""" --- Pract 1 ---
!pip install tensorflow
              
import tensorflow as tf
print("Matrix Multiplication Demo")
x=tf.constant([1,2,3,4,5,6],shape=[2,3])
print(x)
y=tf.constant([7,8,9,10,11,12],shape=[3,2])
print(y)
z=tf.matmul(x,y)
print("Product:",z)
e_matrix_A=tf.random.uniform([2,2],minval=3,maxval=10,dtype=tf.float32,name="matrixA")
print("Matrix A:\\n{}\\n\\n".format(e_matrix_A))
eigen_values_A,eigen_vectors_A=tf.linalg.eigh(e_matrix_A)
print("Eigen Vectors:\\n{}\\n\\nEigen Values:\\n{}\\n".format(eigen_vectors_A,eigen_values_A))



        """)

    elif num =="2":
        print(""" --- Pract 2  ---

import numpy as np
from keras.models import Sequential
from keras.layers import Dense

#create a model
model = Sequential()

# adding layers to the model
model.add(Dense(units = 2, activation = 'relu', input_dim = 2))
model.add(Dense(units = 1, activation = 'sigmoid' ))

#configuration of the model
model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics=['accuracy'])

# x = inputs and y = output labels (xor TT)
x = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([0,1,1,0])

# get model weights then train
model.get_weights()
model.fit(x,y,epochs = 500)

pred = model.predict(x)
print(pred)


                            
        """)

    elif num =="3":
        print(""" --- Pract 3  ---
              
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd

names = ["No. of pregnancies","Glucose level","Blood Pressure","skin thickness","Insulin","BMI","Diabetes pedigree","Age","Class"]

df = pd.read_csv ("diabetes.csv")
df.head()

#create model
binaryc = Sequential()

#create layers in the model or NN
binaryc.add(Dense(units=10,activation='relu',input_dim=8))
binaryc.add(Dense(units=8,activation='relu'))
binaryc.add(Dense(units=1,activation='sigmoid'))

binaryc.compile(loss='binary_crossentropy',optimizer='adam',metrics=["accuracy"])

x = df.iloc[:,:-1]
y = df.iloc[:,-1]

from sklearn.model_selection import train_test_split

xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size = 0.25,random_state = 1)

xtrain.shape

ytrain.shape

binaryc.fit(xtrain, ytrain, epochs = 200, batch_size = 20)

predict = binaryc.predict(xtest)
predict.shape

#binary classification
class_label = []

for i in predict:
    if (i >= 0.5):
        class_label.append(1)
    else:
        class_label.append(0)

#print accuracy score
from sklearn.metrics import accuracy_score

print("Accuracy : ", accuracy_score(ytest,class_label))

                            
        """)
    
    elif num =="4a":
        print(""" --- Pract 4a  ---
              
# Cell 1: Import necessary libraries
from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
import numpy as np


# Cell 2: Generate synthetic data
X, Y = make_blobs(n_samples=100, centers=2, n_features=2, random_state=1)

# Scale the input features
scalar = MinMaxScaler()
scalar.fit(X)
X = scalar.transform(X)


# Cell 3: Define and compile the model
model = Sequential()
model.add(Dense(4, input_dim=2, activation='relu'))
model.add(Dense(4, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam')


# Cell 4: Train the model
model.fit(X, Y, epochs=400)


# Cell 5: Generate new synthetic data for prediction
X_new, Y_real = make_blobs(n_samples=3, centers=2, n_features=2, random_state=1)
X_new = scalar.transform(X_new)


# Cell 6: Predict and print results
Y_pred = np.round(model.predict(X_new).flatten())
for i in range(len(X_new)):
    print("X=%s, Predicted=%s, Desired=%s" % (X_new[i], Y_pred[i], Y_real[i]))

                            
        """)
    
    elif num =="4b":
        print(""" --- Pract 4b  ---
              
from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
import numpy as np


X,Y=make_blobs(n_samples=100,centers=2,n_features=2,random_state=1)
scalar=MinMaxScaler()
scalar.fit(X)
X=scalar.transform(X)
model=Sequential()
model.add(Dense(4,input_dim=2,activation='relu'))
model.add(Dense(4,activation='relu'))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam')
model.fit(X,Y,epochs=400)


# Generate new synthetic data for prediction
X_new, Y_real = make_blobs(n_samples=3, centers=2, n_features=2, random_state=1)
X_new = scalar.transform(X_new)

# Predict and print results
Y_prob = model.predict(X_new).flatten()
Y_class = np.round(Y_prob)
for i in range(len(X_new)):
    print("X=%s, Predicted_probability=%s, Predicted_class=%s" % (X_new[i], Y_prob[i], Y_class[i]))
                            
        """)
    
    elif num =="4c":
        print(""" --- Pract 4c  ---
              
from keras.models import Sequential
from keras.layers import Dense
from sklearn.datasets import make_regression
from sklearn.preprocessing import MinMaxScaler

X,Y=make_regression(n_samples=100,n_features=2,noise=0.1,random_state=1)
scalarX,scalarY=MinMaxScaler(),MinMaxScaler()


scalarX.fit(X)
scalarY.fit(Y.reshape(100,1))
X=scalarX.transform(X)
Y=scalarY.transform(Y.reshape(100,1))


model=Sequential()
model.add(Dense(4,input_dim=2,activation='relu'))
model.add(Dense(4,activation='relu'))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='mse',optimizer='adam')
model.fit(X,Y,epochs=1000,verbose=0)


Xnew,a=make_regression(n_samples=3,n_features=2,noise=0.1,random_state=1)
Xnew=scalarX.transform(Xnew)


Ynew=model.predict(Xnew)
for i in range(len(Xnew)):
    print("X=%s,Predicted=%s"%(Xnew[i],Ynew[i]))
                            
        """)
    
    elif num =="5a":
        print(""" --- Pract 5a  ---
              
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from keras.models import Sequential
from keras.layers import Dense
from scikeras.wrappers import KerasRegressor

 
# Load the dataset correctly, skipping the first row (header)
dataframe = pd.read_csv("housing.csv", sep=',', header=0)
print("Shape of dataset:", dataframe.shape)
print("First few rows of dataset:")
print(dataframe.head())
 
# Extract features (X) and target variable (Y)
X = dataframe.drop(columns=['MEDV']).values # Features (all columns except 'MEDV')
Y = dataframe['MEDV'].values              #Target variable ('MEDV')
 
# Check the shape of X (number of features)
print("Shape of X (features):", X.shape)
 
# Define the wider model function
def wider_model():
   model = Sequential()
   model.add(Dense(15,input_dim=X.shape[1], kernel_initializer='normal' , activation='relu'))
   model.add(Dense(13, kernel_initializer='normal', activation='relu'))
   model.add(Dense(1, kernel_initializer='normal'))
   model.compile(loss='mean_squared_error', optimizer='adam')
   return model
 
estimators = []     #Create pipeline with standardization and Keras model
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp',KerasRegressor(build_fn=wider_model, epochs=100, batch_size=5)))
pipeline = Pipeline(estimators)

# Define KFold cross-validation
kfold = KFold(n_splits=10, shuffle=True, random_state=42)


try:                          # Evaluate pipeline using cross-validation
   results = cross_val_score(pipeline, X, Y, cv=kfold)
   print("Wider: %.2f (%.2f) MSE" % (results.mean(), results.std()))
except ValueError as e:
   print("Error during cross-validation:", e)


              

print("Wider: %.2f (%.2f) MSE" % (results.mean(), results.std()))
                            
        """)

    elif num =="5b":
        print(""" --- Pract 5b  ---
              
# Cell 1
from sklearn.datasets import make_classification
from sklearn.model_selection import KFold
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score

              
# Cell 2
# Generate a random multiclass classification dataset
X, y = make_classification(n_samples=100,
                          n_features=20,
                          n_informative=2,
                          n_redundant=0,
                          n_classes=2,
                         n_clusters_per_class=2,
                          random_state=42)

y = to_categorical(y)      # Convert the target variable to categorical format

              
# Cell 3
# Define the k-fold cross-validator
n_splits = 5
kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

model = Sequential()          # Define the feed-forward deep network model
model.add(Dense(64, activation='relu', input_shape=(X.shape[1],)))
model.add(Dense(64, activation='relu'))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

fold_accuracies = []            # Perform k-fold cross-validation

              
# Cell 4
for train_index, val_index in kf.split(X):
   X_train, X_val = X[train_index], X[val_index]
   y_train, y_val = y[train_index], y[val_index]
   model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))
   y_pred_prob = model.predict(X_val)
   y_pred = y_pred_prob.argmax(axis=1)  # Get the predicted class index with highest probability
   accuracy = accuracy_score(y_val.argmax(axis=1), y_pred)
   fold_accuracies.append(accuracy)

              
# Cell 5
# Calculate the mean accuracy across all folds
mean_accuracy = sum(fold_accuracies) / len(fold_accuracies)
print(f'Mean accuracy: {mean_accuracy:.2f}')


                            
        """)

    elif num =="6a":
        print(""" --- Pract 6a  ---
              
from matplotlib import pyplot
from sklearn.datasets import make_moons
from keras.models import Sequential
from keras.layers import Dense
X,Y=make_moons(n_samples=100,noise=0.2,random_state=1)
n_train=30
trainX,testX=X[:n_train,:],X[n_train:]
trainY,testY=Y[:n_train],Y[n_train:]
#print(trainX)
#print(trainY)
#print(testX)
#print(testY)
model=Sequential()
model.add(Dense(500,input_dim=2,activation='relu'))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
history=model.fit(trainX,trainY,validation_data=(testX,testY),epochs=1000)

pyplot.plot(history.history['accuracy'],label='train')
pyplot.plot(history.history['val_accuracy'],label='test')
pyplot.legend()
pyplot.show()
           
                            
        """)

    elif num =="6b":
        print(""" --- Pract 6b  ---
              
from matplotlib import pyplot
from sklearn.datasets import make_moons
from keras.models import Sequential
from keras.layers import Dense
from keras.regularizers import l2

X,Y=make_moons(n_samples=100,noise=0.2,random_state=1)
n_train=30
trainX,testX=X[:n_train,:],X[n_train:]
trainY,testY=Y[:n_train],Y[n_train:]
#print(trainX)
#print(trainY)
#print(testX)
#print(testY)
model=Sequential()
model.add(Dense(500,input_dim=2,activation='relu',kernel_regularizer=l2(0.001)))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
history=model.fit(trainX,trainY,validation_data=(testX,testY),epochs=1000)

              
pyplot.plot(history.history['accuracy'],label='train')
pyplot.plot(history.history['val_accuracy'],label='test')
pyplot.legend()
pyplot.show()              

                            
        """)

    elif num =="6c":
        print(""" --- Pract 6c  ---
              
from matplotlib import pyplot
from sklearn.datasets import make_moons
from keras.models import Sequential
from keras.layers import Dense
from keras.regularizers import l1_l2
X,Y=make_moons(n_samples=100,noise=0.2,random_state=1)
n_train=30
trainX,testX=X[:n_train,:],X[n_train:]
trainY,testY=Y[:n_train],Y[n_train:]
#print(trainX)
#print(trainY)
#print(testX)
#print(testY)
model=Sequential()
model.add(Dense(500,input_dim=2,activation='relu',kernel_regularizer=l1_l2(l1=0.001,l2=0.001)))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
history=model.fit(trainX,trainY,validation_data=(testX,testY),epochs=400)
pyplot.plot(history.history['accuracy'],label='train')
pyplot.plot(history.history['val_accuracy'],label='test')
pyplot.legend()
pyplot.show()

                            
        """)
    
    elif num =="7":
        print(""" --- Pract 7  ---
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler

# Load training data
dataset_train = pd.read_csv('Google_Stock_Price_Train.csv')
training_set = dataset_train.iloc[:, 1:2].values

# Scale the training data
sc = MinMaxScaler(feature_range=(0, 1))
training_set_scaled = sc.fit_transform(training_set)

# Prepare training data
X_train, Y_train = [], []
for i in range(60, 1258):
    X_train.append(training_set_scaled[i-60:i, 0])
    Y_train.append(training_set_scaled[i, 0])
X_train, Y_train = np.array(X_train), np.array(Y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Build the LSTM model
regressor = Sequential()
regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))
regressor.add(Dense(units=1))
regressor.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
regressor.fit(X_train, Y_train, epochs=150, batch_size=32)

              

# Load test data
dataset_test = pd.read_csv('Google_Stock_Price_Test.csv')
real_stock_price = dataset_test.iloc[:, 1:2].values

# Concatenate training and test data for preprocessing
dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis=0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1, 1)

# Scale the test data
inputs = sc.transform(inputs)

# Prepare test data
X_test = []
for i in range(60, 80):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Predict stock prices
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# Plot the results
plt.plot(real_stock_price, color='red', label='Real Google Stock Price')
plt.plot(predicted_stock_price, color='blue', label='Predicted Stock Price')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()

                            
        """)
    
    elif num =="8":
        print(""" --- Pract 8  ---
import keras
from keras import layers
from keras.datasets import mnist
import numpy as np

encoding_dim = 32
# This is our input image
input_img = keras.Input(shape=(784,))
# "encoded" is the encoded representation of the input
encoded = layers.Dense(encoding_dim, activation='relu')(input_img)
# "decoded" is the lossy reconstruction of the input
decoded = layers.Dense(784, activation='sigmoid')(encoded)
# Creating autoencoder model
autoencoder = keras.Model(input_img, decoded)
# Create the encoder model
encoder = keras.Model(input_img, encoded)
encoded_input = keras.Input(shape=(encoding_dim,))
# Retrieve the last layer of the autoencoder model
decoder_layer = autoencoder.layers[-1]
# Create the decoder model
decoder = keras.Model(encoded_input, decoder_layer(encoded_input))
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

              
# Scale and make train and test dataset
(X_train, _), (X_test, _) = mnist.load_data()
X_train = X_train.astype('float32') / 255.
X_test = X_test.astype('float32') / 255.
X_train = X_train.reshape((len(X_train), np.prod(X_train.shape[1:])))
X_test = X_test.reshape((len(X_test), np.prod(X_test.shape[1:])))
print(X_train.shape)
print(X_test.shape)
# Train autoencoder with training dataset
autoencoder.fit(X_train, X_train,
                epochs=50,
                batch_size=256,
                shuffle=True,
                validation_data=(X_test, X_test))

              
encoded_imgs = encoder.predict(X_test)
decoded_imgs = decoder.predict(encoded_imgs)

import matplotlib.pyplot as plt

n = 10  # How many digits we will display
plt.figure(figsize=(40, 4))
for i in range(10):
    # Display original
    ax = plt.subplot(3, 20, i + 1)
    plt.imshow(X_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    
    # Display encoded image
    ax = plt.subplot(3, 20, i + 1 + 20)
    plt.imshow(encoded_imgs[i].reshape(8, 4))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    
    # Display reconstruction
    ax = plt.subplot(3, 20, 2 * 20 + i + 1)
    plt.imshow(decoded_imgs[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

plt.show()

                            
        """)

    elif num =="9":
        print(""" --- Pract 9  ---
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
import matplotlib.pyplot as plt

              
# Download MNIST data and split into train and test sets
(X_train, Y_train), (X_test, Y_test) = mnist.load_data()

# Plot the first image in the dataset
plt.imshow(X_train[0])
plt.show()
print(X_train[0].shape)

# Reshape the input data
X_train = X_train.reshape(60000, 28, 28, 1)
X_test = X_test.reshape(10000, 28, 28, 1)

# One-hot encode the labels
Y_train = to_categorical(Y_train)
Y_test = to_categorical(Y_test)
print(Y_train[0])

              
# Create a Sequential model
model = Sequential()

# Add model layers
# Learn image features
model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(28, 28, 1)))
model.add(Conv2D(32, kernel_size=3, activation='relu'))
model.add(Flatten())
model.add(Dense(10, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=3)

              
# Predict and print the probabilities for the first 4 images in the test set
print(model.predict(X_test[:4]))

# Print the actual labels for comparison
print(Y_test[:4])

                            
        """)
    
    elif num =="10":
        print(""" --- Pract 10  ---
import keras
from keras.datasets import mnist
from keras import layers
import numpy as np
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt

              
# Load and preprocess the MNIST dataset
(X_train, _), (X_test, _) = mnist.load_data()
X_train = X_train.astype('float32') / 255.
X_test = X_test.astype('float32') / 255.
X_train = np.reshape(X_train, (len(X_train), 28, 28, 1))
X_test = np.reshape(X_test, (len(X_test), 28, 28, 1))

# Add noise to the images
noise_factor = 0.5
X_train_noisy = X_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=X_train.shape)
X_test_noisy = X_test + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=X_test.shape)

# Clip the noisy images to [0, 1]
X_train_noisy = np.clip(X_train_noisy, 0., 1.)
X_test_noisy = np.clip(X_test_noisy, 0., 1.)

# Visualize some noisy images
n = 10
plt.figure(figsize=(20, 2))
for i in range(1, n + 1):
    ax = plt.subplot(1, n, i)
    plt.imshow(X_test_noisy[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()

              
# Build the autoencoder model
input_img = keras.Input(shape=(28, 28, 1))
x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
x = layers.MaxPooling2D((2, 2), padding='same')(x)
x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
encoded = layers.MaxPooling2D((2, 2), padding='same')(x)
x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(encoded)
x = layers.UpSampling2D((2, 2))(x)
x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = layers.UpSampling2D((2, 2))(x)
decoded = layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)
autoencoder = keras.Model(input_img, decoded)

# Compile the autoencoder model
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

# Train the autoencoder model
autoencoder.fit(X_train_noisy, X_train, epochs=3, batch_size=128, shuffle=True,
                validation_data=(X_test_noisy, X_test),
                callbacks=[TensorBoard(log_dir='/tmo/tb', histogram_freq=0, write_graph=False)])

              

# Make predictions using the trained autoencoder model
predictions = autoencoder.predict(X_test_noisy)

# Visualize the denoised images
m = 10
plt.figure(figsize=(20, 2))
for i in range(1, m + 1):
    ax = plt.subplot(1, m, i)
    plt.imshow(predictions[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()

                            
        """)


   

    else:
        print("Invalid input")

#prog('5b')
        
        