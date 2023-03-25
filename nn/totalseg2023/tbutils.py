
# ref 
# https://keras.io/guides/customizing_what_happens_in_fit
# https://gist.github.com/joelthchao/ef6caa586b647c3c032a4f84d52e3a11
# https://stackoverflow.com/questions/43784921/how-to-display-custom-images-in-tensorboard-using-keras
# https://www.tensorflow.org/api_docs/python/tf/summary/image
# https://www.tensorflow.org/tensorboard/migrate
# https://raw.githubusercontent.com/pangyuteng/cycle-gan-apes/main/tbutils.py

import os
import sys
import gc
import random
import numpy as np
from data_gen import NUM_CLASSES
import tensorflow as tf
import json
import datetime
import imageio
from tensorflow import keras
import tensorflow.keras.backend as K


class ImageSummaryCallback(tf.keras.callbacks.Callback):
    def __init__(self, data_gen, logdir):
        super(ImageSummaryCallback, self).__init__()
        self.logdir = logdir
        self.file_writer = tf.summary.create_file_writer(self.logdir)
        self.tstamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.count = 0
        self.epoch = 0
        self.data_gen = data_gen

    def on_batch_end(self, batch, logs=None):
        self.on_end("batch", batch)
        # garbage collection https://github.com/tensorflow/tensorflow/issues/31312#issuecomment-821809246
        #gc.collect()
        #K.clear_session()

    def on_epoch_end(self, epoch, logs=None):        
        self.epoch = epoch
        self.on_end("epoch", epoch)
        gc.collect()
        K.clear_session()

    def on_end(self, kind, batch, logs=None):        
        os.makedirs('images', exist_ok=True)
        # self.data_gen.on_epoch_end()

        for n, items in zip(range(1),self.data_gen):

            cutout_x, mask = items
            y_hat = self.model(cutout_x)
            y_hat = np.argmax(y_hat,axis=-1)

        mask = np.argmax(mask,axis=-1)
        unique_y_true = np.unique(mask).tolist()
        unique_y_pred = np.unique(y_hat).tolist()
        mydict = dict(
            kind=kind,
            count=self.count,
            unique_y_true=unique_y_true,
            unique_y_pred=unique_y_pred,
        )
        with open(os.path.join(self.logdir,f"y-{self.tstamp}.json"),'a+') as f:
            f.write(json.dumps(mydict)+"\n")

        idx = 8
        row0 = np.concatenate([
            cutout_x[0,:,:,idx].squeeze(),
            mask[0,:,:,idx].squeeze()/NUM_CLASSES,
            y_hat[0,:,:,idx].squeeze()/NUM_CLASSES,
        ],axis=1)

        merged_img = (255*row0).clip(0,255).astype(np.uint8)
        merged_img = np.expand_dims(merged_img,axis=-1)
        
        if kind == 'epoch':
            fname = f"images/{batch:04d}_end.png"
        else:
            fname = f"images/{self.epoch:04d}_{batch:04d}.png"
        imageio.imwrite(fname,merged_img)

        merged_img = np.expand_dims(merged_img,axis=0)
        with self.file_writer.as_default():
            tf.summary.image("sample", merged_img, step=self.count)
            self.file_writer.flush()
            self.count+=1

class MetricSummaryCallback(tf.keras.callbacks.Callback):
    def __init__(self, logdir):
        super(MetricSummaryCallback, self).__init__()
        self.logdir = logdir
        self.file_writer = tf.summary.create_file_writer(self.logdir)
        self.count = 0
        self.tstamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def on_batch_end(self, batch, logs=None):
        self.on_end("batch", batch, logs)

    def on_epoch_end(self, epoch, logs=None):
        self.on_end("epoch", epoch, logs)

    def on_end(self, kind, epoch, logs):
        if logs is not None:
            mydict = dict(logs)
        else:
            mydict = {}

        with self.file_writer.as_default():
            for name, value in mydict.items():
                tf.summary.scalar(name, value, step=self.count)
                self.file_writer.flush()

        mydict['count']=self.count
        mydict['kind']=kind
        with open(os.path.join(self.logdir,f"metrics-{self.tstamp}.json"),'a+') as f:
            f.write(json.dumps(mydict)+"\n")
        self.count+=1
