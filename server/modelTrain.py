def train_model():
    import tensorflow as tf
    import numpy as np
    import random
    import math
    import os
    #import cv2

    DIR = "../WasteImagesDataset/"
    IMG_SIZE = (256, 256)
    train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        DIR,
        validation_split=0.1,
        subset="training",
        seed=42,
        batch_size=16,
        image_size=IMG_SIZE
    )

    test_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        DIR,
        validation_split=0.1,
        subset="validation",
        seed=42,
        batch_size=16,
        image_size=IMG_SIZE
    )

    classes = train_dataset.class_names
    numClasses = len(train_dataset.class_names)
    print(classes, numClasses)

    AUTOTUNE = tf.data.AUTOTUNE
    train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
    test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)

    from keras.layers import Rescaling, RandomFlip, RandomRotation
    from keras.applications.inception_v3 import preprocess_input
    from keras.layers import GlobalAveragePooling2D
    
    data_augmentation = tf.keras.Sequential([
        Rescaling(1./255),
        RandomFlip("horizontal_and_vertical"),
        RandomRotation(0.2),
    ])

    preprocess_input = preprocess_input
    global_average_layer = GlobalAveragePooling2D()

    # Define your model architecture
    baseModel = tf.keras.applications.ResNet152(input_shape=(256, 256, 3), weights='imagenet',
                                                include_top=False, classes=numClasses)

    for layer in baseModel.layers:
        layer.trainable = False

    last_output = baseModel.layers[-1].output



    x = tf.keras.layers.Dropout(0.5)(last_output)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    x = tf.keras.layers.Dense(numClasses, activation='softmax')(x)

    model = tf.keras.Model(inputs=baseModel.input, outputs=x)

    # Compile the model
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
    loss = tf.keras.losses.SparseCategoricalCrossentropy()

    model.compile(optimizer=optimizer,
                  loss=loss,
                  metrics=['accuracy'])

    # Train the model
    epochs = 10
    callbacks = tf.keras.callbacks.EarlyStopping(patience=2)
    history = model.fit(train_dataset, validation_data=test_dataset, epochs=epochs, callbacks=[callbacks])

    # Save the trained model
    model.save("retrained_model.keras")

def retrain_model():
    import tensorflow as tf
    import numpy as np

    # Load the saved model
    #model = tf.keras.models.load_model("../simple_keras.keras")
    model = tf.keras.models.load_model("retrained_model.keras")

    DIR = "../WasteImagesDataset/"
    NEW_IMAGE_DIR = "../NewImagesDataset/"
    IMG_SIZE = (256, 256)

    train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        NEW_IMAGE_DIR,
        validation_split=0.1,
        subset="training",
        seed=42,
        batch_size=16,
        image_size=IMG_SIZE
    )

    test_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        NEW_IMAGE_DIR,
        validation_split=0.1,
        subset="validation",
        seed=42,
        batch_size=16,
        image_size=IMG_SIZE
    )

    classes = train_dataset.class_names
    numClasses = len(train_dataset.class_names)
    print(classes, numClasses)

    AUTOTUNE = tf.data.AUTOTUNE
    train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
    test_dataset = test_dataset.prefetch(buffer_size=AUTOTUNE)

    from keras.layers import Rescaling, RandomFlip, RandomRotation, RandomBrightness, RandomContrast
    from keras.applications.inception_v3 import preprocess_input
    from keras.layers import GlobalAveragePooling2D
    
    data_augmentation = tf.keras.Sequential([
        RandomFlip("horizontal"),
        RandomRotation(0.2),
        RandomContrast(0.2),
        RandomBrightness(0.2)
    ])

    train_dataset = train_dataset.map(lambda x, y: (data_augmentation(x, training=True), y))

    model.trainable = False

    # Assuming train_dataset and test_dataset are already defined

    # # Print the shape of the input data just before training
    # sample_input = next(iter(train_dataset))  # Get a sample input from the training dataset
    # img_array, label = sample_input  # Assuming the input data is a tuple (image, label)
    # print("Shape of input data in new dataset:", img_array.shape)


    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
    loss = tf.keras.losses.SparseCategoricalCrossentropy()

    model.compile(optimizer=optimizer,
                  loss=loss,
                  metrics=['accuracy'])

    # Train the model
    epochs = 10
    callbacks = tf.keras.callbacks.EarlyStopping(patience=2)
    history = model.fit(train_dataset, validation_data=test_dataset, epochs=epochs, callbacks=[callbacks])

    # Save the retrained model
    model.save("retrained_model.keras")

if __name__ == "__main__":
    train_model()
    #retrain_model()