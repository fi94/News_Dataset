import json,os
import argparse
from skimage import io
import shutil
import string

def read_json(file_name):
    data = json.load(open(file_name, 'r'))
    return data


def parse_args():
    parser = argparse.ArgumentParser(description='parameter of dataset')
    parser.add_argument('--data_json_1w', default='news_dataset/data_info_1w.json', help='experiment configure file name')
    parser.add_argument('--data_json_2w', default='news_dataset/data_info_2w.json', help='experiment configure file name')
    parser.add_argument('--data_root', default='news_dataset',help='experiment configure file name')
    parser.add_argument('--output_dir1', default='news_dataset/output_dataset_file/daily_news', help='experiment configure file name')
    parser.add_argument('--output_dir2', default='news_dataset/output_dataset_file/outbreak_news', help='experiment configure file name')
    args = parser.parse_args()
    return args


def clean_data(item):
    if len(item['object_annotation']) > 0 and len(item['sentence_annotation']) > 0:
        return 1
    else:
        return 0

def get_annotation_info(annotation):
    if '第一批' in annotation:
        image_file_name = '一万张第一批数据'
    elif '第二批' in annotation:
        image_file_name = '一万张第二批数据'
    else:
        image_file_name = None
        print(image_file_name)
    news_file = annotation.split('—')[-1].split('.')[0].strip(string.digits)
    return news_file, image_file_name


if __name__ == "__main__":
    args = parse_args()
    data1 = read_json(args.data_json_1w)
    data2 = read_json(args.data_json_2w)
    print(len(data1), len(data2))
    # 统计新闻类型
    counter = {}
    for item1 in data1:
        counter[item1['news_type']] = counter.get(item1['news_type'], 0) + 1
    for item2 in data2:
        counter[item2['news_type']] = counter.get(item2['news_type'], 0) + 1

    print(counter)
    # 将其分成突发和日常
    Daily_news = ['社会', '奇趣', '旅游', '军事', '文娱', '科教', '体育']

    Outbreak_news = ['空难', '游行', '暴乱', '火灾', '地震', '坍塌', '爆炸', '山体滑坡', '台风', '泥石流', '洪灾', '交通事故', '海啸', '龙卷风', '洪水', '泥石流', '灾难现场']
    print(len(Outbreak_news), len(Daily_news))
    Daily_news_info = []
    Outbreak_news_info = []
    for item1 in data1:
        if item1['news_type'] in Daily_news:
            flag = clean_data(item1)
            if flag == 1:
                Daily_news_info.append(item1)
        if item1['news_type'] in Outbreak_news:
            flag = clean_data(item1)
            if flag == 1:
                Outbreak_news_info.append(item1)
    for item2 in data2:
        if item2['news_type'] in Daily_news:
            flag = clean_data(item2)
            if flag == 1:
                Daily_news_info.append(item2)
        if item2['news_type'] in Outbreak_news:
            flag = clean_data(item2)
            if flag == 1:
                Outbreak_news_info.append(item2)
    print(len(Daily_news_info), len(Outbreak_news_info))

    # counter2 = {}
    # for dn in Daily_news_info:
    #     counter2[dn['news_type']] = counter2.get(dn['news_type'], 0) + 1
    #
    # counter3 = {}
    # for on in Outbreak_news_info:
    #     counter3[on['news_type']] = counter3.get(on['news_type'], 0) + 1
    #
    # print(counter2)
    # print(counter3)
    final_output_daily = []
    i = 0
    counter_daily_error = 0
    for dn in Daily_news_info:
        image_path = os.path.join(args.data_root, 'project_2w', dn['image_path'])
        try:
            img = io.imread(image_path)
        except Exception as e:
            # print(e)
            img = None
            counter_daily_error += 1
            print(image_path)
            continue
        if img is not None:
            new_image_path = os.path.join(args.output_dir1, 'images', 'image_' + str(i) + '.' + image_path.split('.')[-1])
            dn['original_path'] = image_path
            dn['image_path'] = new_image_path
            # 复制图片
            # shutil.copyfile(image_path, new_image_path)
            final_output_daily.append(dn)
            i += 1
    j = 0
    final_output_outbreak = []
    counter_outbreak_error = 0
    for on in Outbreak_news_info:
        if 'image_path' in on.keys():
            image_path = os.path.join(args.data_root, 'project_2w', on['image_path'])
            try:
                img = io.imread(image_path)
            except Exception as e:
                print(e)
                print(image_path)
                counter_outbreak_error += 1
                img = None
                continue
            if img is not None:
                new_image_path = os.path.join(args.output_dir2, 'images',
                                              'image_' + str(j) + '.' + image_path.split('.')[-1])
                on['original_path'] = image_path
                on['image_path'] = new_image_path
                # 复制图片
                # shutil.copyfile(image_path, new_image_path)
                final_output_outbreak.append(on)
                j += 1
        else:
            # 根据annotation_path的信息找image的位置
            news_file, image_file_name = get_annotation_info(on['annotation_path']) # news_file: 新闻类型； image_file_name：一万张第一批数据
            image_list =[(image_name.split('.')[0],image_name.split('.')[-1]) for image_name in os.listdir(os.path.join(args.data_root, image_file_name, news_file))]
            for (name, suffix) in image_list:
                if on['image_name'] == name:
                    image_name_all = os.path.join(args.data_root, image_file_name, news_file, on['image_name'] + '.' + suffix)
                    try:
                        img = io.imread(image_name_all)
                    except Exception as e:
                        print(e)
                        print(image_name_all)
                        img = None
                        continue
                    if img is not None:
                        new_image_path = os.path.join(args.output_dir2, 'images',
                                                      'image_' + str(j) + '.' + suffix)
                        on['original_path'] = image_name_all
                        on['image_path'] = new_image_path
                        # 复制图片
                        # shutil.copyfile(image_name_all, new_image_path)
                        final_output_outbreak.append(on)
                        j += 1

    print(len(final_output_outbreak), len(final_output_daily))
    print(counter_daily_error, counter_outbreak_error)
    # 保存
    with open(os.path.join(args.output_dir1, 'daily_info.json'), 'w') as f:
        json.dump(final_output_daily, f)


    with open(os.path.join(args.output_dir2, 'outbreak_info.json'), 'w') as f:
        json.dump(final_output_outbreak, f)
