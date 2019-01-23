import re


def extract_email(s, line):
    email = None
    match = re.search(r'[\w\.-]+@[\w\.-]+', line)
    if match is not None:
        email = match.group(0)
    return email


def extract_sex(parts, line):
    sex_found = False
    sex = None
    for w in parts:
        if 'sex' in w:
            sex_found = True
            continue
        if sex_found and ':' not in w:
            if w == 'male':
                sex = 'male'
            else:
                sex = 'female'
            break
    return sex


def extract_education(parts, line):
    found = False
    education = None
    for w in parts:
        # print(w)

        if 'education' in w :
            found = True
            continue
        if found and ':' not in w:
            education = w
            break
    return education

def extract_summary(parts, line):
    found = False
    summary = None
    for w in parts:
        # print(w)

        if 'summary' in w :
            found = True
            continue
        if found and ':' not in w:
            summary = w
            break
    return summary

def extract_knowledge(parts, line):
    found = False
    knowledge = None
    for w in parts:
        # print(w)

        if 'knowledge' in w :
            found = True
            continue
        if found and ':' not in w:
            knowledge = w
            break
    return knowledge

def extract_project(parts, line):
    found = False
    project = None
    for w in parts:
        # print(w)

        if 'project' in w :
            found = True
            continue
        if found and ':' not in w:
            project = w
            break
    return project


def extract_mobile(parts, line):
    found = False
    mobile = None
    i=0
    # while(i<len(parts)):
    #     w=parts[i]
    #     i=i+1
    for w in parts:
        # print(w)

        # if 'mobile' in w or 'phone' in w or 'contact':
        # f=False
        # match=re.search(r'[\d]{10,15}', w)
        # if match is not None:
        #     f=True
        # if w.find('mobile') != -1 or w.find('phone') != -1: 
        #     # print(mobile,'--',parts[i])
        #     found = True
        #     # mobile=w
        #     continue
        # if found: # and ':' not in w:
            # match = re.search(r'[\d]{10,15}', w)
            # if match is not None:
            #     mobile=w
            #     break
        match = re.search(r'[\d]{10,15}', w)
        if match is not None:
            (a,b)=match.span()
            mobile=w[a:b]
            break
        

        # print(mobile)
    return mobile


def extract_experience(parts, line):
    found = False
    result = None
    for w in parts:
        if w.find('experience') != -1 :
            found = True
            continue
        if found and ':' not in w:
            result = w
            break
    return result


def extract_expertise(parts, line):
    length = 4
    line = line.lower()
    index = line.find('know')
    if index == -1:
        length = 2
        index = line.find('familiar')
    if index == -1:
        length = 2
        index = line.find('use')
    if index == -1:
        length = 2
        index = line.find('master')
    if index == -1:
        length = 4
        index = line.find('understand')
    if index == -1:
        length = 4
        index = line.find('develop')

    result = None
    if index == -1:
        return None
    else:
        result = line[index + length:].replace(':', '').strip()
        if result == '':
            return None
    return result


def extract_ethnicity(parts, line):
    race_found = False
    race = None
    for w in parts:
        if w.find('race') != -1 or w.find('religion') != -1:
            race_found = True
            continue
        if race_found and w.find(':') == -1:
            race = w
            break
    return race


def extract_name(parts, line):
    found = False
    result = None
    for w in parts:
        if w.find('name') != -1 :
            found = True
            continue
        if found and w.find(':') == -1:
            result = w
            break
    return result


def extract_objective(parts, line):
    found = False
    result = None
    for w in parts:
        if w.find('objective') != -1 :
            found = True
            continue
        if found and ':' not in w:
            result = w
            break
    return result
