'''Trains a simple convnet on the MNIST dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

from __future__ import print_function
import pickle as pkl
import tensorflow as tf
import keras
from keras.layers import Input, Conv2D, Dense, MaxPooling2D, Flatten, Reshape, Embedding
from keras.models import Model
from keras import backend as K
from keras.engine.topology import Layer
from keras.engine import InputSpec
from keras import losses
import numpy as np

batch_size = 1
num_classes = 10
epochs = 12

img_rows, img_cols = 600, 128  # input image dimensions
img_shape = (img_rows, img_cols, 1)

data = pkl.load(open('./wordvec/embedding.pkl', 'rb'))
dictionary = data.pop('dictionary')
embedding = data.pop('embedding')
data2 = pkl.load(open('./wordvec/review_cnn_600.pkl', 'rb'))
user_rev = data2.pop('user_review')
busi_rev = data2.pop('busi_review')
data3 = pkl.load(open('./wordvec/review_extract.pkl', 'rb'))
user_busi_star = data3.pop('user_busi_star')
del data, data2, data3

data_num = 0  # 4235
for u in user_busi_star:
    for b in user_busi_star[u]:
        data_num += 1
y_total = np.ndarray([data_num, 1])

k = 0
for u in user_busi_star:
    for b in user_busi_star[u]:
        y_total[k] = user_busi_star[u][b]
        k += 1
x1_total = np.ndarray([data_num, img_shape[0]], dtype='float32')
x2_total = np.ndarray([data_num, img_shape[0]], dtype='float32')
k = 0
for u in user_busi_star:
    for b in user_busi_star[u]:
        for ii, word in enumerate(user_rev[u].split(' ')):
            index = dictionary.get(word, 0)
            x1_total[k, ii] = index
        for jj, word in enumerate(busi_rev[b].split(' ')):
            index = dictionary.get(word, 0)
            x2_total[k, jj] = index
        k += 1

test_rate = int(data_num / 5)
y_test = y_total[:test_rate]
y_train = y_total[test_rate:]
x1_test = x1_total[:test_rate]
x1_train = x1_total[test_rate:]
x2_test = x2_total[:test_rate]
x2_train = x2_total[test_rate:]

print('x1_train shape:', x1_train.shape)
print(x1_train.shape[0], 'train samples')
print(x1_test.shape[0], 'test samples')
print(x1_test.shape)
print(x2_test.shape)
print(x1_test[1, :].shape)


class FM(Layer):
    def __init__(self, output_dim=1, k=10, **kwargs):
        self.output_dim = output_dim
        self.k = k
        super(FM, self).__init__(**kwargs)
    
    def build(self, input_shape):
        assert len(input_shape) >= 2
        input_dim = input_shape[-1]
        # Create a trainable weight variable for this layer.
        self.w2 = self.add_weight(name='interact',
                                  shape=(input_shape[1], self.k),
                                  initializer='glorot_uniform',
                                  trainable=True)
        self.kernel = self.add_weight(name='kernel',
                                      shape=(input_shape[1], self.output_dim),
                                      initializer='glorot_uniform',
                                      trainable=True)
        self.bias = self.add_weight(shape=(self.output_dim,),
                                    initializer='zeros',
                                    name='bias',
                                    trainable=True)
        self.input_spec = InputSpec(min_ndim=2, axes={-1: input_dim})
        self.built = True
        super(FM, self).build(input_shape)  # Be sure to call this somewhere!
    
    def call(self, inputs):
        output = K.dot(inputs, self.kernel)
        output = K.bias_add(output, self.bias)
        in_dim = int(inputs.shape[-1])  # in_dim = int(input_shape[-1])
        print(output.shape)
        print(inputs.shape[-1])
        print(inputs.shape)
        print('======')
        w2_new = tf.reshape(tf.tile(self.w2, [batch_size, 1]), [-1, in_dim, self.k])
        board_x = tf.reshape(tf.tile(inputs, [1, self.k]), [-1, in_dim, self.k])
        board_x2 = tf.square(board_x)
        q = tf.square(tf.reduce_sum(tf.multiply(w2_new, board_x), axis=1))
        h = tf.reduce_sum(tf.multiply(tf.square(w2_new), board_x2), axis=1)
        output += 1 / 2 * tf.reduce_sum(q - h, axis=1)
        return output
    
    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)


class Embedding_dan(Layer):
    def __init__(self, output_dim=img_cols, input_length=None, **kwargs):
        self.output_dim = output_dim
        self.input_length = input_length
        super(Embedding_dan, self).__init__(**kwargs)
    
    def build(self, input_shape):
        input_dim = input_shape[-1]
        # Create a trainable weight variable for this layer.
        self.embeddings = self.add_weight(name='kernel',
                                          shape=(embedding.shape[0], self.output_dim),
                                          initializer=self.my_init,
                                          trainable=False)
        self.input_spec = InputSpec(min_ndim=2, axes={-1: input_dim})
        self.built = True
        super(Embedding_dan, self).build(input_shape)  # Be sure to call this somewhere!
    
    def call(self, inputs):
        if K.dtype(inputs) != 'int32':
            inputs = K.cast(inputs, 'int32')
        output = K.gather(self.embeddings, inputs)
        return output
    
    def compute_output_shape(self, input_shape):
        if self.input_length is None:
            return input_shape + (self.output_dim,)
        else:
            # input_length can be tuple if input is 3D or higher
            if isinstance(self.input_length, (list, tuple)):
                in_lens = list(self.input_length)
            else:
                in_lens = [self.input_length]
            if len(in_lens) != len(input_shape) - 1:
                ValueError('"input_length" is %s, but received input has shape %s' %
                           (str(self.input_length), str(input_shape)))
            else:
                for i, (s1, s2) in enumerate(zip(in_lens, input_shape[1:])):
                    if s1 is not None and s2 is not None and s1 != s2:
                        ValueError('"input_length" is %s, but received input has shape %s' %
                                   (str(self.input_length), str(input_shape)))
                    elif s1 is None:
                        in_lens[i] = s2
            return (input_shape[0],) + tuple(in_lens) + (self.output_dim,)
    
    def my_init(shape, dtype=None):
        return embedding


def train():
    # Headline input: meant to receive sequences of 100 integers, between 1 and 10000.
    # Note that we can name any layer by passing it a "name" argument.
    input1 = Input(shape=(img_rows,), dtype='float32', name='input1')
    # vec1 = tf.nn.embedding_lookup(embedding, input1)
    vec1 = Embedding_dan()(input1)
    print(vec1.shape)
    vec1 = Reshape([600, 128, 1])(vec1)
    x1 = Conv2D(32, kernel_size=(3, 128), activation='relu',
                input_shape=img_shape)(vec1)
    x1 = MaxPooling2D(pool_size=(6, 1))(x1)
    x1 = Flatten()(x1)
    output1 = Dense(128, activation='relu', name='output1')(x1)
    
    input2 = Input(shape=(img_rows,), dtype='float32', name='input2')
    # vec2 = tf.nn.embedding_lookup(embedding, input2)
    vec2 = Embedding_dan()(input2)
    vec2 = Reshape([600, 128, 1])(vec2)
    x2 = Conv2D(32, kernel_size=(3, 3), activation='relu',
                input_shape=img_shape)(vec2)
    x2 = MaxPooling2D(pool_size=(2, 2))(x2)
    x2 = Flatten()(x2)
    output2 = Dense(128, activation='relu', name='output2')(x2)
    
    con_x = keras.layers.concatenate([output1, output2])
    
    # output = Lambda(FM,output_shape=1, name='output')(con_x)
    # output = Dense(10, activation='softmax', name='output')(con_x)
    output = FM(1, name='output')(con_x)
    
    model = Model(inputs=[input1, input2], outputs=output)
    
    model.compile(optimizer='rmsprop', loss=losses.mae, metrics=['accuracy'])
    # model.compile(loss=keras.losses.categorical_crossentropy,
    #              optimizer=keras.optimizers.Adadelta(),
    #              metrics=['accuracy'])
    # And trained it via:
    model.fit({'input1': x1_train, 'input2': x2_train}, y_train,
              epochs=epochs, batch_size=batch_size, verbose=1,
              validation_data=({'input1': x1_test, 'input2': x2_test}, y_test))
    
    score = model.evaluate({'input1': x1_test, 'input2': x2_test}, y_test,
                           verbose=0, batch_size=batch_size)
    # pred = model.predict({'input1':x1_test,'input2':x2_test})
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    
    model.save('./wordvec/my_model.h5')
    
    
def predict():
    from keras.models import load_model

    model = load_model('./wordvec/my_model.h5', custom_objects={'Embedding_dan': Embedding_dan, 'FM': FM})
    #
    # a = x1_test[0, :]
    # b = x2_test[0, :]
    # a.shape = (1, 600)
    # b.shape = (1, 600)
    # print(a.shape)
    # preds = model.predict({'input1': a, 'input2': b}, batch_size=batch_size)
    #
    # print(preds)
    fp = open('result.json', 'w')
    a = np.ndarray([1, img_shape[0]], dtype='float32')
    b = np.ndarray([1, img_shape[0]], dtype='float32')
    print(len(busi_rev))
    print(len(user_rev))
    i = 0
    for buf_user in user_rev.items():
        i += 1
        print(i)
        result = {}
        user_id = buf_user[0]
        user_review = buf_user[1]
        result['user_id'] = user_id
        result['value'] = []
        for buf_busi in busi_rev.items():
            busi_id = buf_busi[0]
            busi_review = buf_busi[1]
            for ii, word in enumerate(user_review.split(' ')):
                index = dictionary.get(word, 0)
                a[0, ii] = index
            for jj, word in enumerate(busi_review.split(' ')):
                index = dictionary.get(word, 0)
                b[0, jj] = index
            a.shape = (1, 600)
            b.shape = (1, 600)
            preds = model.predict({'input1': a, 'input2': b}, batch_size=batch_size)
            result['value'].append({'busi_id': busi_id, 'value': preds[0][0]})
            # print(user_id, busi_id, preds[0][0])
        fp.write(str(result) + '\n')
    fp.close()
            


predict()




