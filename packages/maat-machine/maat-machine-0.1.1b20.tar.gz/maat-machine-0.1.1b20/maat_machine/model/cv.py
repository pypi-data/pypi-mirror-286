from types import NoneType
from typing import Union

import os
import copy
import pathlib as paths
import zipfile
import tempfile
import joblib

import json
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras as ktf
import keras
from keras import models as mktf
from keras import layers as lktf
from keras import optimizers as oktf
from keras import preprocessing as ppktf
from keras import utils as uktf
from keras import losses as lsktf
import tensorflow.keras.preprocessing.image as tkpi
import sklearn.base as sk_base
import sklearn.model_selection as sk_modsel

from keras import regularizers

from PIL import Image as pillow_images

from IPython.display import display


class CNNCustomClassifier(sk_base.BaseEstimator, sk_base.ClassifierMixin):
    def __init__(self,
                 num_classes, input_shape,
                 epochs, batch_size,
                 optimizer, loss,
                 validation_split,

                 file_path_column_name,
                 label_column_name,

                 conv_layer_array,
                 conv_kernel_size_default,
                 conv_activation, conv_activation_parameter,
                 conv_pool_size, conv_dropout,

                 dense_layer_array,
                 dense_activation, dense_activation_parameter,
                 dense_dropout):
        self.num_classes = num_classes
        self.input_shape = input_shape
        self.epochs = epochs
        self.batch_size = batch_size
        self.optimizer = optimizer
        self.loss = loss
        self.validation_split=validation_split

        self.file_path_column_name = file_path_column_name
        self.label_column_name = label_column_name

        self.conv_layer_array = conv_layer_array
        self.conv_kernel_size_default = conv_kernel_size_default
        self.conv_activation = conv_activation
        self.conv_activation_parameter = conv_activation_parameter
        self.conv_pool_size = conv_pool_size
        self.conv_dropout = conv_dropout

        self.dense_layer_array = dense_layer_array
        self.dense_activation = dense_activation
        self.dense_activation_parameter = dense_activation_parameter
        self.dense_dropout = dense_dropout

        self.model = None
        self.image_data_generator = None
        self.train_generator = None
        self.validation_generator = None
        self.test_generator = None

        self.class_indices = None

    def __getstate__(self):
        state = self.__dict__.copy()

        if 'optimizer' in state:
            del state['optimizer']
        if 'model' in state:
            del state['model']
        if 'image_data_generator' in state:
            del state['image_data_generator']
        if 'train_generator' in state:
            del state['train_generator']
        if 'validation_generator' in state:
            del state['validation_generator']
        if 'test_generator' in state:
            del state['test_generator']

        return state

    def create_cnn_model(self):
        model = keras.Sequential()
        model.add(lktf.Input(shape=self.input_shape, name='input'))

        for i, conv_layer_config in list(enumerate(self.conv_layer_array)):
            conv_filters_i, conv_kernel_i, layers_i = conv_layer_config
            assert 'c' in layers_i
#             if i == 0:
#                 model.add(lktf.Conv2D(filters=conv_filters_i, kernel_size=(1, 1), padding='same'))

            print(f"Conv Layer config: {conv_layer_config}")

            model.add(lktf.Conv2D(
                filters=conv_filters_i, kernel_size=conv_kernel_i,
                padding='same',
#                 kernel_regularizer=regularizers.L2(1e-3),
#                 activity_regularizer=regularizers.L2(1e-3),
                name=f"conv2d-{i}_0"
            ))
#             if 'b' in layers_i:
#                 model.add(lktf.BatchNormalization(name=f"batch-{i}_0"))
            model.add(lktf.ReLU(name=f"relu-{i}_0"))
            conv2d_count = layers_i.count('c')
            if conv2d_count > 1:
                for c_i in range(0, conv2d_count-1):
                    model.add(lktf.Conv2D(
                        filters=conv_filters_i, kernel_size=conv_kernel_i,
                        padding='same',
        #                 kernel_regularizer=regularizers.L2(1e-3),
        #                 activity_regularizer=regularizers.L2(1e-3),
                        name=f"conv2d-{i}_{c_i+1}"
                    ))
#                     if 'b' in layers_i:
#                         model.add(lktf.BatchNormalization(name=f"batch-{i}_{c_i+1}"))
                    model.add(lktf.ReLU(name=f"relu-{i}_{c_i+1}"))
        #             model.add(self._obtain_activation(self.conv_activation, self.conv_activation_parameter))
            if 'b' in layers_i:
                model.add(lktf.BatchNormalization(name=f"batch-{i}"))
            if 'p' in layers_i:
                model.add(lktf.MaxPooling2D(pool_size=self.conv_pool_size, padding='same', name=f"max_pooling_2d-{i}"))
            if 'd' in layers_i:
                model.add(lktf.Dropout(self.conv_dropout, name=f"dropout-{i}"))

        model.add(lktf.Flatten(name='flatten'))

        for i, dense_layer_config in list(enumerate(self.dense_layer_array)):
            dense_layer_size_i, layers_i = dense_layer_config
            assert 'e' in layers_i

            if 'b' in layers_i:
                model.add(lktf.BatchNormalization(name=f"dense-batch-{i}"))

            model.add(lktf.Dense(
                dense_layer_size_i,
#                 kernel_regularizer=regularizers.L2(1e-3),
#                 activity_regularizer=regularizers.L2(1e-3),
                name=f"dense-{i}"
            ))
#             model.add(self._obtain_activation(self.dense_activation, self.dense_activation_parameter))
            model.add(lktf.ReLU(name=f"dense-relu-{i}"))

            if 'd' in layers_i:
                model.add(lktf.Dropout(self.dense_dropout, name=f"dense-dropout-{i}"))

        model.add(lktf.Dense(self.num_classes, activation='softmax', name='output'))

        model.compile(
            optimizer=self.optimizer,
            loss=self.loss,
            metrics=['accuracy'],
        )
        self.model = model

        return model

    def _obtain_activation(self, name: str, negative_slope: Union[int, NoneType] = None):
        if name == 'relu':
            return lktf.ReLU(negative_slope=0.0 if negative_slope is None else negative_slope)
        elif name == 'lrelu':
            return lktf.LeakyReLU(negative_slope=0.3 if negative_slope is None else negative_slope)

    def fit(self, features: pd.DataFrame, labels: pd.Series):
        assert (features.index == labels.index).all()
        assert self.file_path_column_name in features
        assert self.label_column_name == labels.name
        assert self.model is not None

        # ImageDataGenerator сам делает преобразование меток, если class_mode='categorical'
        # encoded_labels = pd.Series(
        #     self.one_hot_encoder.transform(labels.values.reshape(-1, 1)).toarray().tolist(),
        #     index=labels.index,
        #     name=self.label_column_name
        # )
        data_frame = pd.concat([features, labels], axis=1)
        display(data_frame.sample(10))
        display(np.unique(labels))

        image_data_generator = tkpi.ImageDataGenerator(
            rescale=1.0/255,
            validation_split=self.validation_split
        )
        self.image_data_generator = image_data_generator

        train_generator = image_data_generator.flow_from_dataframe(
            dataframe=data_frame,
            x_col=self.file_path_column_name,
            y_col=self.label_column_name,
            color_mode="rgb",
            class_mode="categorical",
            target_size=(self.input_shape[0], self.input_shape[1]),
            batch_size=self.batch_size,
            seed=137,
            suffle=True,
            subset='training'
        )
        self.train_generator = train_generator

        validation_generator = image_data_generator.flow_from_dataframe(
            dataframe=data_frame,
            x_col=self.file_path_column_name,
            y_col=self.label_column_name,
            color_mode="rgb",
            class_mode="categorical",
            target_size=(self.input_shape[0], self.input_shape[1]),
            batch_size=self.batch_size,
            seed=137,
            suffle=True,
            subset='validation'
        )
        self.validation_generator = validation_generator

        result = self.model.fit(
            train_generator,
            epochs=self.epochs,
            validation_data=validation_generator,
        )

        self.class_indices = self.train_generator.class_indices
        return result

    def predict_proba_from_dataframe(self, features: pd.DataFrame):
        assert self.file_path_column_name in features
        image_data_generator = tkpi.ImageDataGenerator(rescale=1.0/255)
        test_generator = image_data_generator.flow_from_dataframe(
            dataframe=features,
            directory=None,
            x_col=self.file_path_column_name,
            y_col=None,
            batch_size=self.batch_size,
            seed=42,
            shuffle=False,
            color_mode="rgb",
            class_mode=None,
            target_size=(self.input_shape[0], self.input_shape[1]),
        )
        self.test_generator = test_generator
        return self.model.predict(test_generator)
    
    def predict_from_dataframe(self, features: pd.DataFrame):
        labels_predicted_proba = self.predict_proba_from_dataframe(features)
        labels_predicted = np.argmax(labels_predicted_proba, axis=1)

        label_dict = {v: k for k, v in self.class_indices.items()}

        labels_original_predicted = [label_dict[label] for label in labels_predicted]
        return labels_original_predicted
    
    def score_from_dataframe(self, features: pd.DataFrame, labels_true: pd.Series):
        labels_predicted = self.predict_from_dataframe(features)
        labels_true_array = np.array(labels_true)
        accuracy = np.mean(labels_predicted == labels_true_array) * 100
        return accuracy

    def predict_proba_from_pil_image_raw(self, image: pillow_images.Image):
        target_width = self.input_shape[1]
        target_height = self.input_shape[0]
        test_image = image.resize((target_width, target_height))
        test_image = test_image.convert('RGB')
        image_array = np.array(test_image, dtype='float64') / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        labels_predicted_proba = self.model.predict(image_array)
        return labels_predicted_proba[0]
    
    def predict_proba_from_pil_image(self, image: pillow_images.Image) -> dict:
        labels_predicted_proba = self.predict_proba_from_pil_image_raw(image)
        label_dict = {v: k for k, v in self.class_indices.items()}
        predicted_labels_dict = {
            label_dict[i]: probability for i, probability in enumerate(labels_predicted_proba)
        }
        return predicted_labels_dict

    def predict_from_pil_image(self, image: pillow_images.Image):
        labels_predicted_proba = self.predict_proba_from_pil_image(image)
        predicted_label = max(labels_predicted_proba, key=labels_predicted_proba.get)
        return predicted_label
    
    def get_history(self):
        if self.model:
            return copy.deepcopy(self.model.history.history)
        else:
            return None

    @staticmethod
    def save(instance, directory_path, file_name: str = 'model.zip'):
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save the Keras model
            model_path = os.path.join(tmpdir, "model.keras")
            instance.model.save(model_path, overwrite=True, include_optimizer=False)

            # Save the wrapper class instance
            wrapper_path = os.path.join(tmpdir, "model.wrapper.joblib")
            joblib.dump(instance, wrapper_path)

            # Create a zip file
            with zipfile.ZipFile(f"{directory_path}/{file_name}", 'w') as zipf:
                zipf.write(model_path, arcname="model.keras")
                zipf.write(wrapper_path, arcname="model.wrapper.joblib")

    @staticmethod
    def load(directory_path, file_name: str = 'model.zip'):
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Extract the zip file
            with zipfile.ZipFile(f"{directory_path}/{file_name}", 'r') as zipf:
                zipf.extractall(tmpdir)

            # Load the Keras model
            model_path = os.path.join(tmpdir, "model.keras")
            model = keras.models.load_model(model_path)

            # Load the wrapper class instance
            wrapper_path = os.path.join(tmpdir, "model.wrapper.joblib")
            wrapper = joblib.load(wrapper_path)

            # Update the model in the loaded instance
            wrapper.model = model
            return wrapper

    @staticmethod
    def save_lightweight(instance, directory_path, file_name: str = 'model_lightweight.zip'):
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save the Keras model
            model_json = instance.model.to_json()
            model_path = os.path.join(tmpdir, "model.json")
            with open(str(model_path), 'w') as json_file:
                json_file.write(model_json)
            
            # Save the model weights
            model_weights_path = os.path.join(tmpdir, "model.weights.h5")
            instance.model.save_weights(model_weights_path)

            # Save the wrapper class instance
            wrapper_path = os.path.join(tmpdir, "model.wrapper.joblib")
            joblib.dump(instance, wrapper_path)

            # Create a zip file
            with zipfile.ZipFile(f"{directory_path}/{file_name}", 'w') as zipf:
                zipf.write(model_path, arcname="model.json")
                zipf.write(model_weights_path, arcname="model.weights.h5")
                zipf.write(wrapper_path, arcname="model.wrapper.joblib")
    
    @staticmethod
    def load_lightweight(directory_path, file_name: str = 'model_lightweight.zip'):
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Extract the zip file
            with zipfile.ZipFile(f"{directory_path}/{file_name}", 'r') as zipf:
                zipf.extractall(tmpdir)

            # Load the Keras model
            model_path = os.path.join(tmpdir, "model.json")
            with open(str(model_path), 'r') as json_file:
                model_json = json_file.read()
            model = mktf.model_from_json(model_json)

            # Load the model weights
            model_weights_path = os.path.join(tmpdir, "model.weights.h5")
            model.load_weights(model_weights_path)

            # Load the wrapper class instance
            wrapper_path = os.path.join(tmpdir, "model.wrapper.joblib")
            wrapper = joblib.load(wrapper_path)

            # Update the model in the loaded instance
            wrapper.model = model
            return wrapper