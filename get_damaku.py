import requests, time,os,csv,json
import bilibili_api
import pandas as pd
from bilibili_api import video, sync, Credential
from bilibili_api.exceptions import ResponseCodeException, DanmakuClosedException


def get_danmaku(bvid):
        v = video.Video(bvid)
        print(bvid)
        time.sleep(2.8)
        try:
            dms = sync(v.get_danmakus(0))
        # 敏感视频，关闭弹幕功能
        except DanmakuClosedException:
            dms = []
        except ResponseCodeException:
            dms = []
        except KeyError:
            dms = []
        except Exception:
            dms = []
        # for dm in dms:
        #     print(dm)
        return dms
def save_danmaku(week,bvid,dms):
    if not os.path.exists("data/danmaku/Week{}".format(week)):
        os.makedirs("data/danmaku/Week{}".format(week))
    with open('data/danmaku/Week{}/{}.csv'.format(week,bvid),'w',encoding='utf-8-sig') as f:
        csvfile=csv.writer(f)
        for dm in dms:
            csvfile.writerow([dm.text,])


def get_all_video(dosth,savesth):
    for week in range(101,151):
        bvlist = []
        with open('bvlist/bvlist_week{}.json'.format(week), mode="r") as f:
            bvlist = json.loads(f.read())
            for bv in bvlist:
                dms = dosth(bv)
                savesth(week, bv, dms)
        print(week)


get_all_video(get_danmaku,save_danmaku)

