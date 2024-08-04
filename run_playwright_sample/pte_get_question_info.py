import logging
import os.path

from playwright.async_api import async_playwright, Page, Playwright
from pydantic import BaseModel as PydanticBase
import json
from dataclasses import dataclass
from pprint import pprint

from database import BASE_DIR

root_dir = os.path.join(BASE_DIR, '..')

dir_address = os.path.join(root_dir, 'media/json')
# from playwright.sync_api import sync_playwright, Playwright, Page
logger = logging.getLogger(__file__)


async def get_content_info(page: Page, q_id: str):
    button_role = "switch"
    answ_button = page.locator(f"//button[@role='{button_role}']")
    await answ_button.click()
    trans_class = 'Answer__AnswerText'
    sc = page.locator(f'// p[starts-with(@class, "{trans_class}")] ')
    sc_txt = await sc.inner_text()

    return sc_txt


SITE_BASE_URL = 'https://www-yi.apeuni.com/en/practice/answer_questions/'

user_dir = '/tmp/playwright/1'


async def run(playwright: Playwright, q_id: str):
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = await chromium.launch_persistent_context(user_data_dir=user_dir, headless=False)
    page = await browser.new_page()
    try:
        shop_url = f"{SITE_BASE_URL}{q_id}"
        await page.goto(shop_url)
    except Exception:
        print(f'error in get {q_id} ')
        return {}
    logger.info(f'the page {q_id} open...')
    # other actions...
    data = await get_content_info(page, q_id)
    await browser.close()
    return data


async def get_question_transcript(q_id: str):
    async with async_playwright() as playwright:
        return await run(playwright, q_id)
