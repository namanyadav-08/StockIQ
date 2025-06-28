import keras
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def main(model, array):
    model = keras.saving.load_model(model)

    test_input = array


    scaler = MinMaxScaler(feature_range=(0, 1))
    test_input = scaler.fit_transform(test_input)
    test_input = np.reshape(test_input, (test_input.shape[0],test_input.shape[1], 1))

    prediction = model.predict(test_input)

    prediction = scaler.inverse_transform(prediction)

    return prediction[-1]