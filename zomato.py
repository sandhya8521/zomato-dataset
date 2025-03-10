# -*- coding: utf-8 -*-
"""zomato.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ww-aeZNDadm7WFFdrP22omUEDbMwCgnE
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('/content/zomato.csv' , encoding = 'latin-1')

df

df.head()

df.shape

df.info()

df.describe()

# checking for missing value

df.isnull().sum()

# visulize the missing value

sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
plt.title ('missing value heatmap')
plt.show()

df.columns

# check class distributaion( for classification )
#print(df['target'].value_counts())
# check class balnce

print(df['Restaurant Name'].value_counts())

print(df['Rating color'].value_counts())

print(df['Rating text'].value_counts())

print(df['Price range'].value_counts())

print(df['Average Cost for two'].value_counts())

#visualize class distributaion

sns.countplot(x = 'Average Cost for two' , data = df)

plt.show()

sns.countplot(x = 'Rating color' ,data = df)
plt.show()

df.columns

sns.countplot(x= 'Restaurant Name' , data = df)

sns.barplot(x = 'Restaurant Name' , y = 'Restaurant Name',data = df)
plt.show()

df.columns

sns.countplot(x = 'Switch to order menu' , data = df)
plt.show()

sns.countplot(x = 'Has Online delivery', data = df)
plt.show()

df.columns

# visualize feacture
# univerate  analysis

df['Restaurant Name'].hist(bins=50)
plt.title("Feature Distribution")
plt.xlabel('feature_name')
plt.ylabel('Count')
plt.show()

df['Restaurant ID'].hist(bins = 20)
plt.title("feature distribution")
plt.xlabel('feature name')
plt.ylabel('count')
plt.show()

df['Price range'].hist(bins = 30)
plt.title ("feature distributaion")
plt.xlabel('feature name')
plt.ylabel('count')
plt.show()

df['Average Cost for two'].hist(bins = 30)
plt.title("Restaurant id ")
plt.xlabel('price range')
plt.ylabel('count')
plt.show()

numeric_df = df.select_dtypes(include= np.number)
plt.figure(figsize=(10, 8))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
plt.show()

sns.pairplot(df,hue = 'Average Cost for two', diag_kind = 'kde')
plt.title("pairwise feature realtionships")
plt.show()

df.columns

# prepare data for deep learning
#from sklearn.preprocessing import MinMaxScaler
# feature scaling
from sklearn.preprocessing import MinMaxScaler

# Select only numeric features for scaling
numeric_features = df.select_dtypes(include=np.number).drop('Price range', axis=1)

# Initialize the scaler
scaler = MinMaxScaler()

# Fit and transform the scaler on numeric features only
scaled_features = scaler.fit_transform(numeric_features)

# If you need a DataFrame with scaled features and original non-numeric features:
scaled_df = pd.DataFrame(scaled_features, columns=numeric_features.columns, index=df.index)
final_df = df.drop(columns=numeric_features.columns).join(scaled_df)

# one HOT coding

from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder()
y_encoded = encoder.fit_transform(df[['Average Cost for two']]).toarray()

# Split Data into Train and Test Sets
from sklearn.model_selection import train_test_split # Import train_test_split

X = scaled_features
y = y_encoded

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train

X_test

y_train

X_train

!pip install xgboost
import xgboost as xgb
from xgboost import XGBClassifier

import numpy as np
from sklearn.preprocessing import LabelEncoder

# ... (your existing code) ...

# Before fitting the model
le = LabelEncoder()
y_train_encoded = le.fit_transform(np.argmax(y_train, axis=1))  # Encode the target variable

# Train XGBoost for feature importance
model = XGBClassifier().fit(X_train, y_train_encoded)  # Use the encoded target

# ... (rest of your code) ...

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

# Assuming X_train and y_train are already defined and accessible
# If not, ensure the cells where they are defined are executed before this one

# Reduce dimensions using PCA
pca = PCA(n_components=2)
x_pca = pca.fit_transform(X_train)

# t-SNE visualization
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X_train)

# Plot t-SNE results
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=np.argmax(y_train, axis=1), cmap='viridis')
plt.title("t-SNE visualization")
plt.colorbar()
plt.show()

from imblearn.over_sampling import SMOTE
import numpy as np

# Calculate the minimum number of samples in any minority class
min_samples = np.min(np.bincount(np.argmax(y_train, axis=1)))

# Set k_neighbors to be the minimum between min_samples - 1 and the desired k_neighbors
k_neighbors = min(min_samples - 1, 5)  # Assuming you initially wanted 5 neighbors

# Handle cases where k_neighbors is invalid
if k_neighbors < 1:
    print("Warning: Minority class with very few samples. Switching to RandomOverSampler.")
    from imblearn.over_sampling import RandomOverSampler
    ros = RandomOverSampler(random_state=42)
    X_resampled, y_resampled = ros.fit_resample(X_train, np.argmax(y_train, axis=1))
else:
    smote = SMOTE(random_state=42, k_neighbors=k_neighbors)
    X_resampled, y_resampled = smote.fit_resample(X_train, np.argmax(y_train, axis=1))

print("Resampling completed successfully.")



#Analyze Dataset for Neural Network Input

 #Distribution of Input Values


plt.hist(X_train.flatten(),bins=50)

plt.show()

sns.boxplot(data=X_train)
plt.title("Feature Boxplot")
plt.show()

import tensorflow as tf # Import TensorFlow
# Load MNIST dataset
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()

# Visualize random image
plt.imshow(X_train[0], cmap='gray')
plt.title(f"Label: {y_train[0]}")
plt.show()

# Normalize pixel values
X_train = X_train / 255.0
X_test = X_test / 255.0

# Check distribution of pixel values
plt.hist(X_train.flatten(), bins=50)
plt.title("Pixel Value Distribution")
plt.show()