from PIL import Image,ImageMath
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread, imsave

from skimage import io
from skimage.color import rgb2hed
from matplotlib.colors import LinearSegmentedColormap
from skimage import color
from matplotlib.colors import rgb_to_hsv

def test(rgba):
    rgba[0]=1
    rgba[2]=110




def changeColor(rgba):
    if rgba[3] > 0:
     if abs(rgba[0] - 250) < 10:
            rgba[0] = 125
            rgba[1] = 230


fig = plt.figure(figsize=(20,4))


img = io.imread("DA_test2.png")
oImg = img.copy()

ax = fig.add_subplot(251)
ax.imshow(oImg)

img1 = img.copy()
img1[:,:,(0,1)]= img[:,:,(1,0)]*0.95
ax = fig.add_subplot(252)
ax.imshow(img1)


img2 = img.copy()
img2[:,:,(1,2)]= img[:,:,(2,1)]*0.95
ax = fig.add_subplot(253)
ax.imshow(img2)


img3 = img.copy()
img3[:,:,(0,2)]= img[:,:,(2,0)]*0.95
ax = fig.add_subplot(254)
ax.imshow(img3)


img4 = img.copy()
img4[:,:,(0,2)]= img[:,:,(2,0)]
img4[:,:,(1)] = 123
ax = fig.add_subplot(255)
ax.imshow(img4)



img = io.imread("DA_aaa.png")


ax = fig.add_subplot(256)
oImg = img.copy()
ax.imshow(oImg)



img1 = img.copy()
img1[:,:,(0,1)]= img[:,:,(1,0)]*0.95
ax = fig.add_subplot(257)
ax.imshow(img1)


img2 = img.copy()
img2[:,:,(1,2)]= img[:,:,(2,1)]*0.95
ax = fig.add_subplot(258)
ax.imshow(img2)


img3 = img.copy()
img3[:,:,(0,2)]= img[:,:,(2,0)]*0.95
ax = fig.add_subplot(259)
ax.imshow(img3)


img4 = img.copy()
img4[:,:,(0,2)]= img[:,:,(2,0)]
img4[:,:,(1)] = 123
ax = fig.add_subplot(2,5,10)
ax.imshow(img4)



plt.show()



#mask = img[:,:,(0,1)]

b1 = 210
b2 = 229


# w , h ,a= img.shape
# for x in range(w):
#     for y in range(h):
#         rgba = img[x][y]
#         if rgba[3] > 0 :
#             des = rgba[0] - 255
#             des2 = rgba[1] - 180
#             if abs(des) < 20 :
#                 # rgba[0] = 72
#                 # rgba[1] = 90
#                 rgba[0] = 80
#                 rgba[2] = 210 + des
#             # if abs(des2) < 30:
#             #     # rgba[0] = 176
#             #     # rgba[1] = 168
#             #     rgba[2] = 229 + des


# io.imshow(img)
# io.imsave("DA_test3.png",img)
# io.show()

# cmap_hema = LinearSegmentedColormap.from_list('mycmap', ['white', 'navy'])
# cmap_dab = LinearSegmentedColormap.from_list('mycmap', ['white',
#                                              'saddlebrown'])
# cmap_eosin = LinearSegmentedColormap.from_list('mycmap', ['darkviolet',
#                                                'white'])
# img = io.imread("DA_test2.png")
# ihc_rgb = img
# ihc_hed = rgb2hed(ihc_rgb)
# fig, axes = plt.subplots(2, 2, figsize=(7, 6), sharex=True, sharey=True,
#                          subplot_kw={'adjustable': 'box-forced'})
# ax = axes.ravel()
#
# ax[0].imshow(ihc_rgb)
# ax[0].set_title("Original image")
#
# ax[1].imshow(ihc_hed[:, :, 0], cmap=cmap_hema)
# ax[1].set_title("Hematoxylin")
#
# ax[2].imshow(ihc_hed[:, :, 1], cmap=cmap_eosin)
# ax[2].set_title("Eosin")
#
# ax[3].imshow(ihc_hed[:, :, 2], cmap=cmap_dab)
# ax[3].set_title("DAB")
#
# for a in ax.ravel():
#     a.axis('off')
#
# fig.tight_layout()
# plt.show()

#io.imsave('DA_test3.png',img)


# @adapt_rgb(each_channel)
# def sobel_each(image):
#     return filters.sobel(image)
#
#
# @adapt_rgb(hsv_value)
# def sobel_hsv(image):
#     return filters.sobel(image)
#
#     return filters.sobel(image)
#
# def as_gray(image_filter, image, *args, **kwargs):
#     gray_image = rgb2gray(image)
#     return image_filter(gray_image, *args, **kwargs)
#
# @adapt_rgb(as_gray)
# def sobel_gray(image):
#         return filters.sobel(image)
#
#
# img = io.imread("DA_test2.png")
#
# fig = plt.figure(figsize=(14, 7))
# ax_each = fig.add_subplot(121, adjustable='box-forced')
# ax_hsv = fig.add_subplot(122, sharex=ax_each, sharey=ax_each,
#                          adjustable='box-forced')
#
#
# ax_each.imshow(rescale_intensity(1 - sobel_each(img)))
# ax_each.set_xticks([]), ax_each.set_yticks([])
# ax_each.set_title("Sobel filter computed\n on individual RGB channels")
#
# # We use 1 - sobel_hsv(image) but this will not work if image is not normalized
# ax_hsv.imshow(rescale_intensity(1 - sobel_gray(img)))
# ax_hsv.set_xticks([]), ax_hsv.set_yticks([])
# ax_hsv.set_title("Sobel filter computed\n on (V)alue converted image (HSV)")
#
# plt.show()