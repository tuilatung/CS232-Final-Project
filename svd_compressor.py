import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import svd
from PIL import Image


def svd_compress(image, k):
    img = image
    
    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]
    
    ur,sr,vr = svd(r, full_matrices=False)
    ug,sg,vg = svd(g, full_matrices=False)
    ub,sb,vb = svd(b, full_matrices=False)
    rr = np.dot(ur[:,:k],np.dot(np.diag(sr[:k]), vr[:k,:]))
    rg = np.dot(ug[:,:k],np.dot(np.diag(sg[:k]), vg[:k,:]))
    rb = np.dot(ub[:,:k],np.dot(np.diag(sb[:k]), vb[:k,:]))

    rimg = np.zeros(img.shape)
    rimg[:,:,0] = rr
    rimg[:,:,1] = rg
    rimg[:,:,2] = rb
    
    for ind1, row in enumerate(rimg):
        for ind2, col in enumerate(row):
            for ind3, value in enumerate(col):
                if value < 0:
                    rimg[ind1,ind2,ind3] = abs(value)
                if value > 255:
                    rimg[ind1,ind2,ind3] = 255

    compressed_image = rimg.astype(np.uint8)
    compressed_image = Image.fromarray(compressed_image)
    return compressed_image


if __name__ == "__main__":

    input_image = np.asarray(Image.open('static/uploads/a.jpg'))
    compress = svd_compress(input_image, k=70)
    plt.imshow(compress)
    plt.show()