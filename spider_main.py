
from playwright.async_api import async_playwright


async def main(url, queue_process_num):
    async def down(input_page):
        async  with input_page.expect_download() as download_info:
            await input_page.locator(".woo-font.woo-font--download").first.click()
        tem_download = await download_info.value
        row_path = await  tem_download.path()
        print(row_path)

        return tem_download

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # main_url ='https://weibo.com/5829182826/Lp2vleY2s'

        # main_url = url

        await page.goto(url)

        await page.wait_for_url(url)
        await page.wait_for_load_state('domcontentloaded')
        await page.wait_for_load_state('load')

        print("============首页加载完成==============")
        # await page.wait_for_load_state('domcontentloaded')
        # await  page.pause()

        await page.click(".woo-box-item-inlineBlock >> nth=0")

        all_image_loca = page.locator(".Viewer_prevItem_McSJ4")
        all_image_num = await all_image_loca.count()
        queue_process_num.put(all_image_num)

        print("=========图片数量===========")
        print(all_image_num)
        print("=========图片数量===========")

        for i in range(all_image_num):
            queue_process_num.put(i)  # 进程通信
            await all_image_loca.nth(i).click()
            await page.wait_for_load_state('domcontentloaded')
            # await page.wait_for_load_state('load')
            download = await down(page)
            image_name = download.suggested_filename
            print(image_name)

            await download.save_as("./save_image/" + image_name)
            print("完成图片数量:" + str(i))
            # await page.pause()
        print("=======================")
        print("========爬虫结束=========")
        await page.close()
        await browser.close()


