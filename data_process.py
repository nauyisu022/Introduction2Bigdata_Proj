import pandas as pd
import os


def _method_get_videos_info_documents(filepath):
    '''
    根据弹幕文件夹名获取当天视频Top100文件（videoTop_xxx.csv)
    :param video_top_file_name:
    :return:
    '''
    video_top_list = []
    for item in method_get_danmu_folders(filepath):
        video_top_list.append("videoTop_" + item)
    return video_top_list


def _method_get_classify_info(video_top_file_name):
    '''
    根据视频信息csv文件，获取视频全部分类
    :param video_top_file_name:
    :return:
    '''
    df = pd.read_csv(video_top_file_name + ".csv", low_memory=False)
    return df['视频分类'].tolist()


def _get_all_topfiles(filepath):
    for root, dirs, files in os.walk(filepath):
        print(files)
        for item in files:
            df = pd.read_csv(filepath + item, low_memory=False)
            print(df['视频分类'])
    # df = pd.read_csv(video_top_file_name + ".csv", low_memory=False)
    # return df['视频分类'].tolist()


if __name__ == '__main__':
    _get_all_topfiles('data/')
# classify_list = []
# for item in _method_get_videos_info_documents("data/"):
#     classify_list.extend(_method_get_classify_info("data/" + item))
# classify_top = collections.Counter(classify_list)
