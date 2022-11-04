import requests, time,os,csv,json
import bilibili_api
import pandas as pd
from bilibili_api import video, sync


HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'referer': 'https://www.bilibili.com/',
    'x-csrf-token': '',
    'x-requested-with': 'XMLHttpRequest',
    'cookie': '',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52'}


def get_week_popular_list(week):
    bvidlist = []
    url = 'https://api.bilibili.com/x/web-interface/popular/series/one?number={}'.format(week)
    req = requests.get(url, headers=HEADERS, timeout=0.5).json()
    time.sleep(0.3)
    list = req['data']['list']
    for item in list:
        bvidlist.append(bilibili_api.aid2bvid(item['aid']))
    if not os.path.exists("bvlist/"):
        os.makedirs("bvlist/")

    with open("bvlist/bvlist_week{}.json".format(week), mode="w") as f:
        json.dump(bvidlist,f)
    return bvidlist



def get_videos_tag(tag_url):
    tag_list = []
    req = requests.get(tag_url, headers=HEADERS, timeout=0.5).json()
    time.sleep(0.5)
    tag_list = req['data']
    return tag_list


def taglist2csv(taglist,name):
    file_path = ("data/tag_{}.csv".format(name))
    f = open(file_path, mode="w", encoding="utf-8-sig", newline='')
    csv_writer2 = csv.DictWriter(f,
                                 fieldnames=['tag_id', 'tag_name']
                                 )
    csv_writer2.writeheader()
    dictfilt = lambda x, y: dict([(i, x[i]) for i in x if i in set(y)])
    wanted_keys = ('tag_id', 'tag_name')
    for tag in taglist:
        csv_writer2.writerow(dictfilt(tag, wanted_keys))
    f.close()


def get_videos_info(bvid):
    # 实例化 Video 类
    v = video.Video(bvid=bvid)
    # 获取视频信息
    info = sync(v.get_info())
    # 打印视频信息
    return info



def get_pop_csvs(start,end):
    taglist = []
    for i in range(start, end):
        bvidList = get_week_popular_list(i)
        file_path = ("data/week_popular_{}.csv".format(i))
        # 判断路径是否存在
        if not os.path.exists("data/"):
            os.makedirs("data/")
        # 如果文件存在，则覆盖写入
        f = open(file_path, mode="w", encoding="utf-8-sig", newline='')
        csv_writer1 = csv.DictWriter(f,
                                     fieldnames=[
                                         '视频bvid', '视频aid', 'videos', '视频分类', '版权所有',
                                         '视频封面', '视频标题', '上传时间', '公开时间', '视频描述',
                                         '播放量', '点赞量','投币量','收藏量']
                                     )
        csv_writer1.writeheader()

        for bvid in bvidList:
            time.sleep(2.5)

            info = get_videos_info(bvid)



            tag_url = 'https://api.bilibili.com/x/web-interface/view/detail/tag?aid={}&cid={}'.format(
                info["aid"], info["cid"]
            )
            taglist += get_videos_tag(tag_url)


            data_dict1 = {
                '视频bvid': info.get('bvid', "None"),
                '视频aid': info.get('aid', "None"),
                'videos': info.get('videos', "None"),
                '视频分类': info.get('tname', "None"),
                '版权所有': info.get('copyright', "None"),
                '视频封面': info.get('pic', "None"),
                '视频标题': info.get('title', "None"),
                '上传时间': info.get('ctime', "None"),
                '公开时间': info.get('pubdate', "None"),
                '视频描述': info.get('desc', "None"),
                '播放量': info.get('stat', "None").get('view', "None"),
                '点赞量': info.get('stat', "None").get('like', "None"),
                '投币量': info.get('stat', "None").get('coin', "None"),
                '收藏量': info.get('stat', "None").get('favorite', "None")
            }
            csv_writer1.writerow(data_dict1)
        f.close()
        print(i)
    taglist2csv(taglist, '{}-{}'.format(start,end))


#get_pop_csvs(1,188)

get_pop_csvs(81,90)


# for i in range(1,188):
#
#     print("week:{}".format(i))






# result = []
# for i in range(1, 10000):
#     url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={}'.format(i)
#
#     req = requests.get(url, headers=HEADERS, timeout=6).json()
#     time.sleep(0.2)  # 延迟，避免太快 ip 被封
#     data = req['data']
#     if data != None:
#         video = (
#             data['aid'],  # 视频编号
#             data['view'],  # 播放量
#             data['danmaku'],  # 弹幕数
#             data['reply'],  # 评论数
#             data['favorite'],  # 收藏数
#             data['coin'],  # 硬币数
#             data['share']  # 分享数
#         )
#         print(i)
#         result.append(video)
# print(result)
