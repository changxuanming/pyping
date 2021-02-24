import requests
import time
import asyncio


def tbtime():
    r1 = requests.get(url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',
                      headers={
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'})
    x = eval(r1.text)
    timeNum = int(x['data']['t'])
    timeStamp = float(timeNum / 1000)
    timeArray = time.localtime(timeStamp + 1.0)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime



async def func():
    while True:
        t = tbtime()
        print('\r{}'.format(t))
        await asyncio.sleep(1)



if __name__ == '__main__':
    asyncio.run(func())