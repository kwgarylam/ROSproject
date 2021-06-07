import cv2
cap = cv2.VideoCapture(0)

def getImg(display = False, size = [480,340]):

    ret, img = cap.read()
    img = cv2.resize(img, (size[0], size[1]))

    if display:
        cv2.imshow('frame', img)
    return img

if __name__ == '__main__':

    while True:

        myframe = getImg(display=True)

        # Press 'q' to quite the program
        if cv2.waitKey(1) == ord('q'):
            break

# Release program resources
cap.release()
cv2.destroyAllWindows()
