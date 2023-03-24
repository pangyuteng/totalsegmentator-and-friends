
import os,sys

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow.keras.backend as K

from data_gen import seed_everything, MySeriGenerator, NUM_CLASSES, IMG_SIZE
seed_everything()
from model import get_model, custom_loss
from tbutils import ImageSummaryCallback, MetricSummaryCallback

if __name__ == '__main__':

    batch_size = 4
    epochs = 100000
    learning_rate = 1e-4
    model = get_model(IMG_SIZE, NUM_CLASSES)
    opt = tf.keras.optimizers.Adam(
        learning_rate=learning_rate,beta_1=0.9,beta_2=0.999,epsilon=1e-07
    )
    model.compile(optimizer=opt, loss=custom_loss(),run_eagerly=True)

    train_gen = MySeriGenerator('train',shuffle=True,augment=True,batch_size=batch_size)
    val_gen = MySeriGenerator('validation',shuffle=True,augment=True,batch_size=batch_size)
    cb_gen = MySeriGenerator('validation',ret_option=1,shuffle=True,augment=True,batch_size=batch_size)
    steps_per_epoch = len(train_gen)//2
    validation_steps = len(val_gen)//2

    logdir = './log'
    metric_cb = MetricSummaryCallback(logdir)
    image_cb = ImageSummaryCallback(cb_gen,logdir)
    tensorboard_cb = keras.callbacks.TensorBoard(
        log_dir=logdir, histogram_freq=0, write_graph=True, write_images=False,
        update_freq='batch', profile_batch=2, embeddings_freq=0)
    backup_and_restore_cb = tf.keras.callbacks.BackupAndRestore(backup_dir="./backup")
    checkpoint_cb = keras.callbacks.ModelCheckpoint(
        "./weights/weights.{epoch:02d}.hdf5", save_best_only=True,mode='min',monitor="val_loss"
    )
    early_stopping_cb = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=20, mode='min')
    reduce_lr_cb = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', factor=0.1, patience=10,
        verbose=1, mode='min', min_delta=0.0001, cooldown=0, min_lr=0)

    callbacks = [
        metric_cb,image_cb,tensorboard_cb,
        backup_and_restore_cb,checkpoint_cb,
        early_stopping_cb,reduce_lr_cb,
    ]

    model.fit(train_gen, validation_data=val_gen,
        steps_per_epoch=steps_per_epoch,validation_steps=validation_steps,
        verbose=2, epochs=epochs,  callbacks=callbacks,
        max_queue_size=1,workers=1,use_multiprocessing=False,
    )
