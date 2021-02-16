from pyppeteer import launch
import datetime
import time
import asyncio

width, height = 1200, 768
time_sc_login = 40  # 二维码扫描时间
click_freq = 0.3  # 点击间隔
repost_order = 0.3  # 页面加载时间


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
    for i in range(5):
        page = await browser.newPage()
        await page.setViewport({"width": width, "height": height})
        await page.goto('https://cart.tmall.com')
        pages.append(page)
    return pages


# maotai J_CheckBox_2738701342774
# test1 :J_CheckBox_2741016942258
async def choose_item(pages):
    for page in pages:
        await page.bringToFront()
        while True:
            try:
                await page.click('[for=J_CheckBox_2741016942258]')
                break
            except:
                await asyncio.sleep(click_freq)
                # logging out not find item


async def settle(pages):
    for page in pages:
        await page.bringToFront()
        while True:
            try:
                await page.click('a[id=J_Go]')
                print('提交订单')
                break
            except:
                await asyncio.sleep(click_freq)
                print('未找到结算按钮')


async def push_order(pages):
    for page in pages:
        await page.bringToFront()
        while True:
            try:
                # await page.click('.btn-area')
                await page.click('.go-btn')
                print('提交订单')
                break
            except:
                print('未找到提交订单按钮')
    print('流程结束')


async def main():
    browser = await launch(
        headless=False,
        args=['--disable-infobars', f'--window-size={width},{height}']
    )
    page = await browser.newPage()
    await login(page)
    pages = await goto_cart_pages(browser)
    await asyncio.sleep(repost_order)
    await choose_item(pages)
    await settle(pages)
    await push_order(pages)

    '''
    print('勾选商品')
    while True:
        try:
            # await page.click('[for=J_CheckBox_2738701342774]')
            await page.click('[for=J_CheckBox_2737638864341]')
            break
        except:
            await asyncio.sleep(click_freq)
            print('未找到需要勾选的商品')
    await asyncio.sleep(repost_order)
    while True:
        try:
            # await page.click('.btn-area')
            await page.click('a[id=J_Go]')
            print('提交订单')
            break
        except:
            print('未找到结算按钮')
    await asyncio.sleep(repost_order)
    while True:
        try:
            # await page.click('.btn-area')
            await page.click('.go-btn')
            print('提交订单')
            break
        except:
            print('未找到提交订单按钮')
    print('流程结束')
    await asyncio.sleep(300)
    print('end this app')
    '''

    await asyncio.sleep(3000)


if __name__ == '__main__':
    # 多browser
    browsers = [main(), main(), main(), main()]
    asyncio.get_event_loop().run_until_complete(asyncio.wait(browsers))
