# mode 0: daily news; mode 1: outbreak news; mode 2: all news
# import json,os
import argparse
import re
import random
import numpy as np
import jieba


def parse_arg():
    parser = argparse.ArgumentParser(description='parameters')
    parser.add_argument('--DataRoot', default='raw_dataset/',
                       help='experiment configure file name')
    parser.add_argument('--dailyInfo', default='raw_dataset/daily_news/daily_info.json',
                       help='experiment configure file name')
    parser.add_argument('--outbreakInfo', default='raw_dataset/outbreak_news/outbreak_info.json',
                       help='experiment configure file name')
    parser.add_argument('--mode', default='0',
                       help='0 is all daily, 1 is all outbreak, 2 is daily and outbreak')
    args = parser.parse_args()
    return args


def read_json(path):
    data = json.load(open(path, 'r'))
    return data


def get_info(image_info):
    # jieba分词
    image_info = image_info.strip('<div>').strip('</div>')
    seg = jieba.lcut(image_info)
    return seg


def encode_info(image_info, vocab_dict):
    image_info = image_info.strip('<div>').strip('</div>')
    seg = jieba.lcut(image_info)
    out_seg = []
    for s in seg:
        out_seg.append(vocab_dict[s])
    return out_seg


def np2list(array_data):
    return array_data.tolist()


def list2np(list_data):
    return np.array(list_data)


def change_path_root(original_path, image_root):
    path = re.sub('news_dataset/output_dataset_file/', image_root, original_path)
    return path

def data_process(daily_data, outbreak_data, mode, args):
    info = []
    if mode == '0':
        data, label, info = process_daily_data(daily_data, args)
    elif mode == '1':
        data, label = process_outbreak_data(outbreak_data, args)
    else:
        data, label = process_all_data(daily_data, outbreak_data, args)
    return data, label, info


def process_daily_data(daily_data, args):
    daily_category = {'社会': 0, '奇趣': 1, '旅游': 2, '军事': 3, '文娱': 4, '科教': 5, '体育': 6}
    data_path = []
    label = []
    info = []
    diction = {}
    for dd in daily_data:
        seg_info = get_info(dd['image_info'])
        for si in seg_info:
            diction[si] = diction.get(si, 0) + 1

    cw = sorted([(count, w) for w, count in diction.items()], reverse=True)
    print('top words and their counts:')
    print('\n'.join(map(str, cw[:20])))
    vocab = [k for k, v in diction.items()]
    vocab_dict = {w: i+1 for i, w in enumerate(vocab)}
    with open('dataset/info_diction.json', 'w') as f:
        json.dump(vocab_dict, f)
    for dd in daily_data:
        image_path = change_path_root(dd['image_path'], args.DataRoot)
        info.append(encode_info(dd['image_info'], vocab_dict))
        data_path.append(image_path)
        label.append(daily_category[dd['news_type']])
    return data_path, label, info


def process_outbreak_data(outbreak_data, args):
    data_path = []
    label = []
    for od in outbreak_data:
        image_path = change_path_root(od['image_path'],args.DataRoot)
        data_path.append(image_path)
        label.append(od['news_type'])
    return data_path, label


def process_all_data(daily_data, outbreak_data, args):
    data_path = []
    label = []
    for od in outbreak_data:
        image_path = change_path_root(od['image_path'], args.DataRoot)
        data_path.append(image_path)
        label.append(od['news_type'])
    for dd in daily_data:
        image_path = change_path_root(dd['image_path'], args.DataRoot)
        data_path.append(image_path)
        label.append(dd['news_type'])
    return data_path, label


def ramdom_data(data, label, info):
    assert len(data) == len(label) and len(data) == len(info), print('Dataset wrong')
    index = [i for i in range(len(data))]
    random.shuffle(index)
    data = list2np(data)
    label = list2np(label)
    info = list2np(info)
    data = data[index]
    label = label[index]
    info = info[index]
    data = np2list(data)
    label = np2list(label)
    info = np2list(info)
    assert len(data) == len(label) and len(data) == len(info), print('Dataset wrong')
    return data, label, info


if __name__ == '__main__':
    args = parse_arg()
    daily_data = read_json(args.dailyInfo)
    outbreak_data = read_json(args.outbreakInfo)
    data, label, info = data_process(daily_data, outbreak_data, mode=args.mode, args=args)

    print(len(data), len(label), len(info))
    output_data, output_label, output_info = ramdom_data(data, label, info)
    train_data = output_data[:int(0.8*len(output_data))]
    test_data = output_data[int(0.8*len(output_data)): int(0.9*len(output_data))]
    val_data = output_data[int(0.9*len(output_data)):]

    train_label = output_label[:int(0.8*len(output_label))]
    test_label = output_label[int(0.8*len(output_label)):int(0.9*len(output_label))]
    val_label = output_label[int(0.9*len(output_label)):]

    train_info = output_info[:int(0.8*len(output_info))]
    test_info = output_info[int(0.8*len(output_info)):int(0.9*len(output_info))]
    val_info = output_info[int(0.9*len(output_info)):]

    for (split, data, label, info) in [('train', train_data, train_label, train_info),
                                       ('test', test_data, test_label, test_info),
                                       ('val', val_data, val_label, val_info)]:
        print(len(data))
        with open(os.path.join('dataset', 'image_path_{}_{}.json'.format(split, args.mode)), 'w') as f:
            json.dump(data, f)
        print(len(label))
        with open(os.path.join('dataset', 'label_{}_{}.json'.format(split, args.mode)), 'w') as f:
            json.dump(label, f)
        print(len(info))
        with open(os.path.join('dataset', 'info_{}_{}.json'.format(split, args.mode)), 'w') as f:
            json.dump(info, f)
