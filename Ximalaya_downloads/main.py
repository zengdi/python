# this script is used to downlaod all audios of Datangshuanglongzhuan

import requests
import json
import pandas as pd
import time
import os

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/67.0.3396.99 Safari/537.36"}


def getAlbumInfo(albumID):
    try:
        albumInfo = requests.get('https://www.ximalaya.com/'
                                 'revision/album/getTracksList?albumId={}&pageNum=1'
                                 .format(albumID), headers=header)
        albumInfo.raise_for_status()
        albumInfo.encoding = albumInfo.apparent_encoding
        info = json.loads(albumInfo.text)
        return info

    except Exception as e:
        print('Error:', e)


def getAudio(albumID, page):
    try:
        audioHtml = requests.get('https://www.ximalaya.com/'
                                 'revision/play/'
                                 'album?albumId={}&pageNum={}&pageSize=30'
                                 .format(albumID, page), headers=header
                                 )
        audioHtml.raise_for_status()
        audioHtml.encoding = audioHtml.apparent_encoding
        info = json.loads(audioHtml.text)
        # print(info)
        tracksAudio = info['data']['tracksAudioPlay']
        audio_info = {}
        for audio in tracksAudio:
            add = audio['src']
            name = audio['trackName']
            index = audio['index']
            audio_info[index] = ({'name': name, 'add': add})
        return audio_info

    except Exception as e:
        print("Error", e)


def getPages(count):
    if count <= 30:
        return 1
    elif count > 30:
        if count % 30 == 0:
            return count / 30
        else:
            return count // 30 + 1


def download(url, savePath, fileName):
    try:
        content = requests.get(url, headers=header).content
        with open(os.path.join(savePath, fileName + '.m4a'), 'wb+') as file:
            file.write(content)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    albumID = 7064547
    albumInfo = getAlbumInfo(albumID)
    totalCount = albumInfo['data']['trackTotalCount']
    pages = getPages(totalCount)
    audios = {}
    for i in range(1, pages + 1):
        data = getAudio(albumID, i)
        audios.update(data)
        time.sleep(2)
    downloads = pd.DataFrame.from_dict(audios, orient='index')
    downloads.to_csv('downloads/audio_add.csv', mode='a+', header=False, encoding='utf-8')
    savePath = 'downloads/audios/'
    i = 1
    for key in audios.keys():
        name = audios[key]['name']
        add = audios[key]['add']
        download(add, savePath, str(key))
        time.sleep(2)
        print('Finshied %s', i / len(audios.keys()))
        i += 1
    print('Downloads finished')
