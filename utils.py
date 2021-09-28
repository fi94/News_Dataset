import json,os


def read_json(data_root, json_file='image.json'):
    # assert data_root == 'news_dataset/tufa_dataset/project_1w/'
    data = []
    for line in open(os.path.join(data_root, json_file), 'r'):
        data.append(json.loads(line))
    return data


# project_1w
def get_data_info(data):
    data_dict = {}
    data_dict['image_size'] = data['task']['task_params']['record']['metadata']['size']
    data_dict['image_path'] = data['task']['task_params']['record']['attachment']
    data_dict[ project_2w'image_info'] = data['task']['task_params']['record']['extraInfoUrls'][0]
    data_dict['news_type'] = data['task_result']['annotations'][0]['input']['value']
    object_list = []
    for object_info in data['task_result']['annotations'][1]['slotsChildren']:
        one_object = {}
        one_object['coordinate'] = object_info['slot']['plane']
        one_object['object_label'] = object_info['children'][0]['input']['value']
        object_list.append(one_object)
    data_dict['object_annotation'] = object_list
    sentence_list = []
    sentence_list.append(data['task_result']['annotations'][2]['input']['value'])
    sentence_list.append(data['task_result']['annotations'][3]['input']['value'])
    data_dict['sentence_annotation'] = sentence_list
    return data_dict


# project_2w
def get_data_info_2w(data):
    data_dict = {}
    data_dict['image_size'] = data['task']['task_params']['record']['metadata']['size']
    data_dict['image_path'] = data['task']['task_params']['record']['attachment']
    if 'extraInfoUrls' in data['task']['task_params']['record'].keys():
        data_dict['image_info'] = data['task']['task_params']['record']['extraInfoUrls'][0]
    else:
        data_dict['image_info'] = 'Miss info'
    # data_dict['news_type'] = data['task_result']['annotations'][0]['input']['value']
    if 'value' in data['task_result']['annotations'][0]['input'].keys():
        data_dict['news_type'] = data['task_result']['annotations'][0]['input']['value']
    else:
        data_dict['news_type'] = 'Miss type'
    object_list = []
    for object_info in data['task_result']['annotations'][1]['slotsChildren']:
        one_object = {}
        one_object['coordinate'] = object_info['slot']['plane']
        if 'value' in  object_info['children'][0]['input'].keys():
            one_object['object_label'] = object_info['children'][0]['input']['value']
        else:
            one_object['object_label'] = 'Miss label'
        object_list.append(one_object)
    data_dict['object_annotation'] = object_list
    sentence_list = []
    sentence_list.append(data['task_result']['annotations'][2]['input']['value'])
    sentence_list.append(data['task_result']['annotations'][3]['input']['value'])
    data_dict['sentence_annotation'] = sentence_list
    return data_dict


# 旧的一万张图片
def get_info_1w(data,annotation_name,image_ann_path):
    data_dict = {}
    object_list = []
    sentence_list = []
    for ann in data['response']['annotations']:
        if ann['type'] == 'document':
            data_dict['news_type'] = ann['attributes']
        else:
            if ann['id'] == None:
                one_object = {}
                one_object['coordinate'] = {'width': ann['width'], 'height': ann['height']}
                one_object['coordinate'].update(ann['vertices'][0])
                one_object['object_label'] = ann['attributes']
                object_list.append(one_object)
            else:
                sentence_list.append(ann['attributes'])
    data_dict['object_annotation'] = object_list
    data_dict['sentence_annotation'] = sentence_list
    data_dict['image_name'] = annotation_name.split('.')[0].split('_')[0]
    data_dict['annotation_path'] = image_ann_path
    return data_dict


if __name__ == '__main__':
    args = parse_args()
    # ======================================================================
    # 第二批日常+突发新闻数据集
    # data_list = read_json(args.data_root, json_file=args.json_dir)
    # # print(len(data_list))
    # data_info_list = []
    # for data in data_list:
    #     data_info = get_data_info(data)
    #     data_info_list.append(data_info)
    # print(len(data_info_list))
    # with open(args.output_dir,'w') as f:
    #     json.dump(data_info_list,f)
    # =======================================================================
    # 第一批突发数据集
    # image_root = ['news_dataset/一万张第一批数据', 'news_dataset/一万张第二批数据']
    annotation_root = ['news_dataset/新闻描述二期第一批数据', 'news_dataset/新闻描述二期第一批数据']
    data_info_list = []
    for annotation in annotation_root:
        news_type_list = [type for type in os.listdir(annotation) if type.split('.')[-1] == 'txt']
        for news_type in news_type_list:
            news_type_path = os.path.join(annotation, news_type)
            for image_ann in os.listdir(news_type_path):
                image_ann_path = os.path.join(annotation, news_type, image_ann)
                data = json.load(open(image_ann_path, 'r'))
                data_info = get_info_1w(data,image_ann,image_ann_path)
                data_info_list.append(data_info)

    print(len(data_info_list))
    print(data_info_list[0])
    with open(args.output_dir,'w') as f:
        json.dump(data_info_list,f)

