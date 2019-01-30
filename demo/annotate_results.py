
import cv2
import os

# colors ={'Name' : [255,255,153], 'Personal' : [255,204,153], 'Summary/Objective' : [255,102,102], 'Education/Qualification/Workshop' : [102,0,51],'Work/Experience' : [102,51,0], 'Project' : [51,0,51], 'Knowledge/Skill' : [102,0,204], 'Certification' : [102,102,0],
#                     'Publication' : [170,102,255], 'Interest/Hobby' : [51,255,51], 'SpokenLanguage' : [51,153,255], 'Trait' : [0,0,204], 'Label' : [51,255,255],'Others' : [160,160,160]}

def annotate_predictions(bboxes,predictions):
    colors ={'Name' : [255,255,153], 'Personal' : [255,204,153], 'Summary/Objective' : [255,102,102], 'Education/Qualification/Workshop' : [102,0,51],'Work/Experience' : [102,51,0], 'Project' : [51,0,51], 'Knowledge/Skill' : [102,0,204], 'Certification' : [102,102,0],
                    'Publication' : [170,102,255], 'Interest/Hobby' : [51,255,51], 'SpokenLanguage' : [51,153,255], 'Trait' : [0,0,204], 'Label' : [51,255,255],'Others' : [160,160,160]}

    # print(bboxes)
    # print('-'*50)
    # print(predictions)

    for name, preds in predictions.items():

        img_dir = name.replace('resume_samples','resume_images')[:-4]
        # print('img_dir :',img_dir)

        sections=bboxes[name]

        i=0
        for img_name in os.listdir(img_dir+'/'):
            # print('img_name :',img_name)
            # print(img_dir)
            # print(sections)
            # print(img_name,'-> ')
            # print(sections[img_name[:-4]])
            if img_name[:-4] in sections.keys():
                bb_img_list=sections[img_name[:-4]]

                img=cv2.imread(img_dir+'/'+img_name)

                # l=15
                # m=15
                for x,y,w,h in bb_img_list:
                    label=preds[i]
                    color=colors[label]
                    # print(label)
                    i+=1

                    # img = cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,255), 2)
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), color, 7)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    # cv2.putText(img,label,(h+x-10,y-8), font, 1,color,2,cv2.LINE_AA)
                    cv2.putText(img,label,(x,y-8), font, 1,color,2,cv2.LINE_AA)

                    # print(x,y,w,h)
                    # cv2.putText(img,label,(h,y+h), font, 2,color,2,cv2.LINE_AA)
                    # l=l+h
                    # m=m+w

                # print('img_name again :',img_name)

                cv2.imwrite(img_dir+'/'+img_name,img)
