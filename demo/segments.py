import numpy as np
import cv2
import sys

class SegmentText(object):
    def __init__(self):
        pass
        
    @classmethod
    def image_resize(cls,image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

            # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized


    def find_segments(self,name=None, resize=False):
        # i=0
        # name='img0.jpg'
        file_content=[]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # fgbg = cv2.createBackgroundSubtractorMOG2()
        import os
        if not os.path.exists(name):
            print(name)
            print("pass correct image name")
            sys.exit(1)
        frame = cv2.imread(name)
        # if frame.all():
        #     print("pass correct image name")
        #     sys.exit(1)

        if resize == True and frame.shape[0] < 1500:
            frame = image_resize(frame, 1500)

        original = frame.copy()
        img = frame.copy()
        img2 = frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # sx,sy=frame.shape

        _, frame = cv2.threshold(frame, 180, 255, cv2.THRESH_BINARY)
        # _, frame = cv2.threshold(frame, 120,255,cv2.THRESH_BINARY_INV)
        # kernel = np.ones((3,3),np.uint8)
        # frame = cv2.erode(frame,kernel,iterations = 1)
        # _, frame = cv2.threshold(frame, 120,255,cv2.THRESH_BINARY_INV)

        frame = cv2.GaussianBlur(frame, (5, 5), 1)
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # fgmask = fgbg.apply(frame)
        # frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        frame = cv2.GaussianBlur(frame, (3, 55), 7)
        _, frame = cv2.threshold(frame, 230, 255, cv2.THRESH_BINARY)

        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        gray = frame
        imgf = gray.copy()

        ret, thresh = cv2.threshold(gray, 180, 255,
                                    cv2.THRESH_BINARY_INV)
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image',thresh)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # Noise removal using Morphological
        # closing operation
        # kernel = np.ones((5, 5), np.uint8)
        # thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
        #                            kernel, iterations=5)

        # kernel = np.ones((5, 11), np.uint8)
        kernel = np.ones((19, 65), np.uint8)

        # Background area using Dialation
        bg = cv2.dilate(thresh, kernel, iterations=1)

        # frame=cv2.GaussianBlur(frame,(1,7),7)

        # kernel = np.ones((1,5), np.uint8)
        # bg = cv2.morphologyEx(bg, cv2.MORPH_CLOSE,
        #                            kernel, iterations=2)

        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', bg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # ret, thresh = cv2.threshold(fg, 127, 255,
        #                             cv2.THRESH_BINARY)
        # print('0')
        image, contours, hierarchy = cv2.findContours(bg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # bg=cv2.threshold(bg,127,255,cv2.THRESH_BINARY_INV)[1]

        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', bg)
        # cv2.waitKey(0)
        # _, contours2 ,_ = cv2.findContours(bg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # contours=contours+contours2

        # img2=img.copy()

        # img1 = cv2.drawContours(img.copy(), contours, -1, (0,0,155), 3)

        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', img1)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print('00')
        bboxes = []
        for c in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[c])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
            if [x, y, w, h] not in bboxes:
                bboxes.append([x, y, w, h])
        
        # print('1')

        if len(bboxes) == 0 :
            return file_content

        # if len(bboxes) == 1:
        #     print(len(contours))
        #     # for c in range(len(contours)):
        #     x, y, w, h = cv2.boundingRect(contours[c])
        #     # print(x, y, w, h)
        #     if h > sx/1.7 and w > sy/1.7 :
        #         i=img2[y:y+w,x:x+h]
        #         print(1)
        #         print(i.shape)
        #         cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        #         cv2.imshow('image', i)
        #         cv2.waitKey(0)
        #         cv2.destroyAllWindows()
        #         image, contours, hierarchy = cv2.findContours(i, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        #         bboxes = []
        #         for c in range(len(contours)):
        #             x, y, w, h = cv2.boundingRect(contours[c])
        #             img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
        #             if [x, y, w, h] not in bboxes:
        #                 bboxes.append([x, y, w, h])


        #     print(c,cv2.isContourConvex(contours[c]))
        # #     epsilon = 0.10*cv2.arcLength(contours[c],True)
        # #     approx = cv2.approxPolyDP(contours[c],epsilon,True)
        #     hull = cv2.convexHull(contours[c])
        #     contours[c]=hull

        # # print(contours)

        # img = cv2.drawContours(im, contours, -1, (155,0,155), 1)

        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print(name.split('.')[0])
        # cv2.imwrite(name.split('.')[0] + '_inter_result.jpg', img)

        bb = np.array(bboxes)

        for x in range(bb.shape[0]):
            bb[x][2] = bb[x][2] + bb[x][0]
            bb[x][3] = bb[x][1] + bb[x][3]

        size = bb.shape[0]

        bb = bb[bb[:, 1].argsort()]

        i = 0
        j = 0
        # merge overlapping
        while i < bb.shape[0]:

            j = i + 1
            if not j < bb.shape[0]:
                break
        #     print(i,j)
        #     print(abs(bb[i][1] - bb[i][3]) ,'--', frame.shape[0]/2)
            if abs(bb[i][1] - bb[i][3]) > frame.shape[0] / 2 or bb[j][1] - bb[j][3] > frame.shape[0] / 2:
                #         print(bb[i][1] - bb[i][3] ,'--', frame.shape[0]/2)
                i = i + 1
                continue
            while j < bb.shape[0]:
                if bb[j][0] < bb[i][2] and bb[j][1] < bb[i][3] and bb[j][0] > bb[i][0] and bb[j][1] > bb[i][1]:
                    bb[i][2] = max(bb[j][2], bb[i][2])
                    bb[i][3] = max(bb[j][3], bb[i][3])

                j = j + 1
            i = i + 1

        i = 0
        # remove concentric
        while i < bb.shape[0]:
            j = i + 1
            while j < bb.shape[0]:
                #         print(i,j)
                if bb[j][0] >= bb[i][0] and bb[j][1] >= bb[i][1] and bb[j][2] <= bb[i][2] and bb[j][3] <= bb[i][3]:
                    #             print(bb[j])
                    bb = np.delete(bb, j, axis=0)
                    j = j - 1

                j = j + 1
            i = i + 1

        import pytesseract
        
        # print('11')

        img3 = img2.copy()
        for b in bb:
            x, y, x2, y2 = b
            img2 = cv2.rectangle(img2, (x, y), (x2, y2), (255, 0, 255), 2)

            i=img2[y:y2,x:x2]
            # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            # cv2.imshow('image',i)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            text=pytesseract.image_to_string(i)
            if text.strip() != '':
                text=text.replace('\n',' ')
                text=text.replace('\t',' ')
                file_content.append(text)
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', img2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # cv2.imwrite(name.split('.')[0] + 'result.jpg', img3)
        
        # cv2.imwrite(name.split('.')[0] + '_inter_result2.jpg',img2)

        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', img2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print('2')

        return file_content

        ###############
        # horizontal merging

        i = 0
        j = 0
        while i < bb.shape[0]:
            j = i + 1
            if not j < bb.shape[0]:
                break
        #     print(i,j)
        #     print(abs(bb[i][1] - bb[i][3]) ,'--', frame.shape[0]/2)
            if abs(bb[i][1] - bb[i][3]) > frame.shape[0] / 2 or bb[j][1] - bb[j][3] > frame.shape[0] / 2:
                #         print(bb[i][1] - bb[i][3] ,'--', frame.shape[0]/2)
                i = i + 1
                continue
            while j < bb.shape[0]:
                if (bb[j][1] + 2 >= bb[i][1] and bb[j][3] - 2 <= bb[i][3]) or (bb[i][1] + 2 >= bb[j][1] and bb[i][3] - 2 <= bb[j][3]):
                    bb[i][0] = min(bb[j][0], bb[i][0])
                    bb[i][1] = min(bb[j][1], bb[i][1])
                    bb[i][2] = max(bb[j][2], bb[i][2])
                    bb[i][3] = max(bb[j][3], bb[i][3])

                    bb = np.delete(bb, j, axis=0)
                    j = j - 1

                j = j + 1
            i = i + 1

        # # remove concentric
        # while i < bb.shape[0]:
        #     j=i+1
        #     while j < bb.shape[0]:
        # #         print(i,j)
        #         if bb[j][0] >= bb[i][0] and bb[j][1] >= bb[i][1] and bb[j][2] <= bb[i][2] and bb[j][3] <= bb[i][3]:
        # #             print(bb[j])
        #             bb= np.delete(bb, j,  axis=0)
        #             j=j-1

        #         j=j+1
        #     i=i+1

        file_content2=[]
        for b in bb:
            x, y, x2, y2 = b
            img3 = cv2.rectangle(img3, (x, y), (x2, y2), (255, 0, 255), 2)
            i=img3[y:y2,x:x2]
            # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            # cv2.imshow('image',i)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            text=pytesseract.image_to_string(i)
            text=text.replace('\n',' ')
            text=text.replace('\t',' ')
            file_content2.append(text)
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', img3)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # cv2.imwrite(name.split('.')[0] + 'result.jpg', img3)
        # return (file_content2)
        return (file_content)




# if __name__ == '__main__':
#     # for x in sys.argv:
#     #     print(x, type(x))
#     if len(sys.argv[:]) == 1:
#         find_segments(name=input('Input image name: '))
#     elif len(sys.argv[1:]) == 2:
#         # print('true')
#         if type(sys.argv[1]) == type(''):
#             # print('resize')

#             find_segments(name=sys.argv[1], resize=True)
#         else:
#             find_segments(name=sys.argv[1], resize=False)
#     else:
#         find_segments(name=sys.argv[1], resize=False)