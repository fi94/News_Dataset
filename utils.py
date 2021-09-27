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



