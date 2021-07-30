import gdown
import os

PATH = 'apps/Sentiment_Analysis/models/'
model_name = 'LSTM_RNN_Sentiment_model.pt'
vocab_name = 'LSTM_RNN_Sentiment_vocab.pkl'

def load():
    if not os.path.exists(PATH + vocab_name):
        # Download Vocab file
        gdown.download(url="https://drive.google.com/uc?id=1USpN8jC8UUKtgMQw3MSVyJVHiqnZZ9XR",
                        output=PATH + vocab_name)
    if not os.path.exists(PATH + model_name):
        #Download Torch model
        gdown.download(url="https://drive.google.com/uc?id=12wibCyhCwt58q8dk8D1XCDMdefNxna88",
                        output=PATH + model_name)
