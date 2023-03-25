from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf
import tensorflow.keras.backend as K
from data_gen import NUM_CLASSES, WH,THICKNESS
from copy import copy
#
# #beautiful. https://github.com/mkocabas/focal-loss-keras/blob/master/focal_loss.py
#
# pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
# pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred)) 
#
# #igore outside lung, per https://arxiv.org/abs/1808.05238
#
# pt_1 = tf.where(tf.logical_and(tf.equal(y_true, 1),y_mask), y_pred, tf.ones_like(y_pred))
# pt_0 = tf.where(tf.logical_and(tf.equal(y_true, 0),y_mask), y_pred, tf.zeros_like(y_pred))
#
def custom_loss(gamma=2., alpha=.25, smooth=1e-7, dice_factor=1e-3):

    def focal_loss_fixed(y_true, y_pred):
        
        y_mask = tf.not_equal(y_true, -1)
        pt_1 = tf.where(tf.logical_and(tf.equal(y_true, 1),y_mask), y_pred, tf.ones_like(y_pred))
        pt_0 = tf.where(tf.logical_and(tf.equal(y_true, 0),y_mask), y_pred, tf.zeros_like(y_pred))
        focal_loss = tf.reduce_mean(
            -K.mean(alpha * K.pow(1. - pt_1, gamma) * K.log(pt_1+K.epsilon())) - K.mean((1 - alpha) * K.pow(pt_0, gamma) * K.log(1. - pt_0 + K.epsilon()))
        )
        
        y_true_f = tf.where(y_mask, y_true, tf.zeros_like(y_true))
        y_pred_f = tf.where(y_mask, y_pred, tf.zeros_like(y_true))
        intersection = K.sum(y_true_f * y_pred_f)
        dice = (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)
        dice_loss = tf.reduce_mean(1.0 - dice)

        total_loss = tf.reduce_mean(focal_loss + dice_factor*dice_loss)
        return total_loss

    return focal_loss_fixed

def ResidualBlock(width):
    def apply(x):
        input_width = x.shape[4]
        if input_width == width:
            residual = x
        else:
            residual = layers.Conv3D(width, kernel_size=1)(x)
        x = layers.BatchNormalization(center=False, scale=False)(x)
        x = layers.Conv3D(
            width, kernel_size=3, padding="same", activation=keras.activations.swish
        )(x)
        x = layers.Conv3D(width, kernel_size=3, padding="same")(x)
        x = layers.Add()([x, residual])
        return x

    return apply

def ResidualBlock(width):
    def apply(x):
        input_width = x.shape[4]
        if input_width == width:
            residual = x
        else:
            residual = layers.Conv3D(width, kernel_size=1)(x)
        x = layers.BatchNormalization(center=False, scale=False)(x)
        x = layers.Conv3D(
            width, kernel_size=3, padding="same", activation=keras.activations.swish
        )(x)
        x = layers.Conv3D(width, kernel_size=3, padding="same")(x)
        x = layers.Add()([x, residual])
        return x

    return apply


def DownBlock(width, block_depth):
    def apply(x):
        x, skips = x
        for _ in range(block_depth):
            x = ResidualBlock(width)(x)
            skips.append(x)
        x = layers.AveragePooling3D(pool_size=2)(x)
        return x

    return apply


def UpBlock(width, block_depth):
    def apply(x):
        x, skips = x
        x = layers.UpSampling3D(size=2)(x) # interpolation="bilinear"
        for _ in range(block_depth):
            x = layers.Concatenate()([x, skips.pop()])
            x = ResidualBlock(width)(x)
        return x

    return apply

# ref residual res net
# https://github.com/keras-team/keras-io/blob/master/examples/generative/ddim.py
# 20a32b18c0b95e914101ec226ef35af9fdac3970

block_depth = 2
res_block_depth = 2
widths = [32, 64, 96, 128]
def get_model(image_size, num_classes):
    inputs = keras.Input(shape=image_size)
    x = layers.Conv3D(widths[0], kernel_size=1)(inputs)
    outputs = layers.Conv3D(num_classes, 
        kernel_size=1, kernel_initializer="zeros",activation="softmax", padding="same")(x)
    return keras.Model(inputs,outputs, name="residual_unet")

def BAKget_model(image_size, num_classes):
    
    inputs = keras.Input(shape=image_size)
    
    x = layers.Conv3D(widths[0], kernel_size=1)(inputs)

    skips = []
    for width in widths[:-1]:
        x = DownBlock(width, block_depth)([x, skips])

    for _ in range(res_block_depth):
        x = ResidualBlock(widths[-1])(x)

    for width in reversed(widths[:-1]):
        x = UpBlock(width, block_depth)([x, skips])

    outputs = layers.Conv3D(num_classes, kernel_size=1, kernel_initializer="zeros",activation="softmax", padding="same")(x)

    return keras.Model(inputs,outputs, name="residual_unet")


if __name__ =="__main__":
    keras.backend.clear_session()
    # Build model
    img_size = (WH,WH,THICKNESS,1)
    num_classes = NUM_CLASSES
    model = get_model(img_size, num_classes)
    model.summary()