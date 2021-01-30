from skimage import io, morphology, img_as_bool, segmentation
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

image = img_as_bool(io.imread('../Images/satImageTest.PNG'))
out = ndi.distance_transform_edt(~image)
out = out < 0.05 * out.max()
out = morphology.skeletonize(out)
out = morphology.binary_dilation(out, morphology.selem.disk(1))
out = segmentation.clear_border(out)
out = out | image

plt.imshow(out, cmap='gray')
plt.imsave('../tmp/gaps_filled.png', out, cmap='gray')
plt.show()
