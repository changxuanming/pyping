from pyppeteer import launch
import datetime
import asyncio
import multiprocessing

width, height = 1200, 768
time_sc_login = 30  # 二维码扫描时间
click_freq = 0.3  # 点击间隔
repost_order = 0.3  # 页面加载时间
BEFORE_SECOND = 1  # 提前2秒开始循环点击


async def login(page):
    await page.setViewport({"width": width, "height": height})
    print(' {}秒扫码登录： !!!!'.format(time_sc_login))
    await page.goto('https://login.tmall.com')
    count = time_sc_login
    while count >= 0:
        print('\r 剩余时间：{}'.format(count), end='')
        count -= 1
        await asyncio.sleep(1)
    print()


async def goto_cart_pages(browser) -> list:
    pages = []
    for i in range(1):
        page = await browser.newPage()
        await page.setViewport({"width": width, "height": height})
        await page.goto('https://cart.tmall.com')
        pages.append(page)
    return pages


# maotai J_CheckBox_2738701342774
# test1 :J_CheckBox_2741016942258
async def choose_item(pages):
    page_url = []
    for page in pages:
        page_url.append(page.url)
    for i in range(len(pages)):
        await pages[i].bringToFront()
        while page_url[i] == pages[i].url:
            try:
                await pages[i].click('[for=J_CheckBox_2741016942258]')
                break
            except:
                await asyncio.sleep(click_freq)
                # logging out not find item


# 结算按钮
async def settle(pages):
    """
    循环所有页面 点击相应的页面
        判断页面相应结果是否是对应的要求
    """
    page_url = []
    for page in pages:
        page_url.append(page.url)
    for i in range(len(pages)):
        await pages[i].bringToFront()
        while page_url[i] == pages[i].url:
            try:
                await pages[i].click('#J_SmallSubmit')
                print('提交结算订单')
            except:
                await asyncio.sleep(click_freq)
                print('未找到结算按钮')


async def push_order(pages):
    page_url = []
    for page in pages:
        page_url.append(page.url)
    for i in range(len(pages)):
        await pages[i].bringToFront()
        while page_url[i] == pages[i].url:
            try:
                # await page.click('.btn-area')
                await pages[i].click('.go-btn')
                print('提交订单')
                break
            except:
                await asyncio.sleep(click_freq)
                print('未找到提交订单按钮')
    print('流程结束')


async def main(buy_time):
    browser = await launch(
        headless=False,
        args=['--disable-infobars', f'--window-size={width},{height}']
    )
    page = await browser.newPage()
    await login(page)
    pages = await goto_cart_pages(browser)

    # 等待抢购
    buy_time = datetime.datetime.strptime(buy_time, '%Y-%m-%d %H:%M:%S')
    wait_second = (buy_time - datetime.datetime.now()).seconds if \
        (buy_time - datetime.datetime.now()).days >= 0 else 0
    print('距离时间还有{}秒'.format(wait_second))
    if wait_second - BEFORE_SECOND > 0:
        await asyncio.sleep(wait_second)

    await choose_item(pages)
    await settle(pages)
    await asyncio.sleep(0.1)
    await push_order(pages)
    await asyncio.sleep(3000)


def start(buy_time):
    n_e_l = asyncio.new_event_loop()
    n_e_l.run_until_complete(main(buy_time))


if __name__ == '__main__':
    buy_time = input('请输入开售时间 【2020-02-06(空格)12:55:50】')
    processes = []
    for i in range(3):
        processes.append(multiprocessing.Process(target=start, args=(buy_time,)))
        processes[i].start()
