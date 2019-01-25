import os


def load_text_label_pairs(data_dir_path, label_type=None):
    if label_type is None:
        label_type = 'line_type'

    result = []

    for f in os.listdir(data_dir_path):
        data_file_path = os.path.join(data_dir_path, f)
        if os.path.isfile(data_file_path) and f.lower().endswith('.txt') and os.path.getsize(data_file_path) > 0:
            with open(data_file_path, mode='rt', encoding='utf8') as file:
                for line in file:
                    # line_type, line_label, sentence = line.strip().split('\t')
                    line_type = line.strip().split('\t')[0]
                    line_label = line.strip().split('\t')[1]
                    sent = line.strip().split('\t')[2:]
                    sentence = ''
                    for x in sent:
                        sentence = sentence + x + ' '
                    if label_type == 'line_type':
                        result.append((sentence, line_type))
                    else:
                        result.append((sentence, line_label))
    return result
