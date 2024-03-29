import pytesseract
import cv2


def compute_img(filename):
    img = cv2.imread(filename)
    h, w, _channel = img.shape
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("gray_" + filename, img)
    img_inv = cv2.bitwise_not(img)
    cv2.imwrite("inv_" + filename, img_inv)

    _, img_bin = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    _, img_bin_inv = cv2.threshold(img_inv, 100, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_data(img_bin, output_type="data.frame")
    text = text[text.conf != -1]

    text_inv = pytesseract.image_to_data(img_bin_inv, output_type="data.frame")
    text_inv = text_inv[text_inv.conf != -1]

    return text_inv
