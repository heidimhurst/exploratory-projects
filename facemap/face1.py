import numpy as np
import cv2

# function to reduce general image
def reduceColors(img, colors, outfile):
    img = cv2.imread(img)
    img = cv2.resize(img, None, fx=0.2, fy=0.2, interpolation = cv2.INTER_CUBIC)
    cv2.imwrite(outfile, img)

    img = cv2.imread(outfile)

    Z = img.reshape((-1, 3))

    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = colors
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))
    # ressm = cv2.resize(res2, (0, 0), fx=0.25, fy=0.25)

    cv2.imwrite(outfile,res2)

# loop to find the most reasonable one
# for i in range(3, 9):
#     outname = "heidi" + str(i) + ".png"
#     reduceColors("heidi.jpg", 5, outname)

reduceColors("littlerichard.jpg", 4, "littlerichard4.jpg")
