from image_processing_mila.utils import io, plot
from image_processing_mila.processing import combination, transformation
import numpy as np
import skimage.color
import skimage.io
import matplotlib.pyplot as plt

# read the images
image1 = io.read_image('c:/users//pacote/images/teste1.jpg')
image2 = io.read_image('c:/users//pacote/images/teste2.jpg')

result_image = combination.transfer_histogram(image1, image2)
plot.plot_result(image1, image2, result_image)

image = skimage.io.imread(fname='c:/users//pacote/images/teste1.jpg', as_gray=True)

#display the image
fig, ax = plt.subplots()
plt.imshow(image, cmap='gray')
plt.show()