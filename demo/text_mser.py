

class SegmentText(object):
    def __init__(self):
        pass
        

    def find_segments(self,name=None):
        import cv2
        import sys
        import numpy as np

        mser = cv2.MSER_create()
        img = cv2.imread(name)
        # img=final

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray,(5,5),0)
        imgf = gray.copy()

        _, thresh = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY_INV)
        thresh = cv2.GaussianBlur(thresh, (5, 5), 11)

        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

        vis = img.copy()
        vis2 = img.copy()
        # mser.detect
        regions, bboxes = mser.detectRegions(thresh)

        hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
        cv2.polylines(vis, hulls, 1, (0, 255, 0))

        # vis=cv2.drawContours(vis, regions, -1, (0, 255, 0), -1)

        # for c in range(len(regions)):
        #     x,y,w,h = cv2.boundingRect(regions[c])
        #     vis = cv2.rectangle(vis,(x,y),(x+w,y+h),(70,255,0),1)

        for x, y, w, h in bboxes:
            #     x,y,w,h = cv2.boundingRect(contours[c])
            vis2 = cv2.rectangle(vis2, (x, y), (x + w, y + h), (70, 255, 0), 1)

        mask = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)
        for contour in hulls:
            cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)
        sy,sx=mask.shape[:2]
        for i in range(0,len(bboxes)):
            x,y,w,h =bboxes[i]
            if h > sy/1.7:
                bboxes[i]=x,y,w,1
        # #     x,y,w,h = cv2.boundingRect(contours[c])
            # mask = cv2.rectangle(mask,(x,y),(x+w,y+h),(0,255,5),2)

        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', mask)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print('1')
        kernel = np.ones((21, 21), np.uint8)

            # Background area using Dialation
        mask = cv2.dilate(mask, kernel, iterations=2)
        
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', mask)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print('2')

        text_only = cv2.bitwise_and(img, img, mask=mask)
        # r,text_only=cv2.threshold(text_only,127,255,cv2.THRESH_BINARY_INV)
        # text_only2=cv2.bitwise_or(img, img, mask=mask)

        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', text_only)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print('3')

        # cv2.imwrite('mser/img.jpg', text_only)

    #     import numpy as np
    #     import cv2
        # from matplotlib import pyplot as plt

        # Image operation using thresholding
        imgO = img.copy()
        # img = cv2.imread('mser/img.jpg')
        img = text_only.copy()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray, 240, 255,
                                    cv2.THRESH_BINARY)

        kernel = np.ones((1, 1), np.uint8)
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,kernel, iterations=2)

        kernel = np.ones((21, 115), np.uint8)
        # _,closing=cv2.threshold(closing,120,255,cv2.THRESH_BINARY_INV)
        kernel = np.ones((15, 21), np.uint8)

        # Background area using Dialation
        bg = cv2.dilate(thresh, kernel, iterations=1)
        # _,bg=cv2.threshold(bg,120,255,cv2.THRESH_BINARY_INV)

        # ret, thresh = cv2.threshold(fg, 127, 255,
        #                             cv2.THRESH_BINARY)
        
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image', bg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print('4')

        image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # img1 = cv2.drawContours(img.copy(), contours, -1, (0,0,155), 3)

        bboxes = []
        for c in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[c])
            img0 = cv2.rectangle(imgO, (x, y), (x + w, y + h), (255, 0, 255), 2)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 5), 2)
            if [x, y, w, h] not in bboxes:
                bboxes.append([x, y, w, h])




        #     print(c,cv2.isContourConvex(contours[c]))
        # #     epsilon = 0.10*cv2.arcLength(contours[c],True)
        # #     approx = cv2.approxPolyDP(contours[c],epsilon,True)
        #     hull = cv2.convexHull(contours[c])
        #     contours[c]=hull

        # # print(contours)

        # img = cv2.drawContours(im, contours, -1, (155,0,155), 1)
        res = name.split('.')[0] + '_mser.jpg'

    #     cv2.imwrite(res, imgO)

        # return res
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.imshow('image', imgO)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        import pytesseract
        file_content=[]
        # print('11')
        if len(bboxes) == 0:
            return file_content

        img3 = img0.copy()
        for b in range(len(bboxes)-1,-1,-1):
            # print(b)
            x, y, x2, y2 = bboxes[b]
            # img2 = cv2.rectangle(img2, (x, y), (x2, y2), (255, 0, 255), 2)

            i=img3[y:y+y2,x:x+x2]
            # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            # cv2.imshow('image',i)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            text=pytesseract.image_to_string(i)
            if text.strip() != '':
                text=text.replace('\n',' ')
                text=text.replace('\t',' ')
                file_content.append(text)

        return file_content


if __name__=="__main__":
    obj=SegmentText()
    c=obj.find_segments('data/resume_images/0.jpg')
    for a in c:
        print(a)
        print('-'*75)
