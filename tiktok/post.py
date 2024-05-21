import time
from typing import TypedDict, Any
import json
import os

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement


class CookieEditorCookie(TypedDict):
    name: str
    value: str
    domain: str
    hostOnly: bool
    path: str
    secure: bool
    httpOnly: bool
    sameSite: str
    session: bool
    firstPartyDomain: str
    partitionKey: Any
    expirationDate: int
    storeId: Any


class TiktokPoster:
    LOGIN_URL = 'https://www.tiktok.com/login/phone-or-email/email'
    UPLOAD_URL = 'https://www.tiktok.com/upload?lang=en'
    HOME = 'https://www.tiktok.com'

    NOT_NOW_BUTTON_SELECTOR = "#tux-portal-container > div:nth-child(2) > div > div > div > div > div.TUXModal.TUXModal--width-Medium.TUXModal--height-undefined.TUXModal--entered > div.jsx-2037160096.content > div.jsx-2037160096.footer > button.css-1ypeuck"
    UPLOAD_INPUT_SELECTOR = "input[type='file']"
    

    def __init__(self, cookies_path: str):
        self.initiate_browser()
        self._login(cookies_path)

    def initiate_browser(self):
        options = ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)

        self.browser = Chrome(options=options)

        self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })

        self.browser.execute_script("setInterval(() => {Object.keys(window).forEach(k => k.match(/^cdc_.*/) && (() => {delete window[k]})())}, 10);")
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            setInterval(() => {
                Object.keys(window).forEach(k => k.match(/^cdc_.*/) && (() => {delete window[k]})())
            }, 10);"""
        })


    def _login(self, cookies_path: str):
        self.browser.get(self.LOGIN_URL)

        time.sleep(3)

        with open(cookies_path) as f:
            sameSiteTranslator = {
                'no_restriction': 'None',
                'lax': 'Lax',
            }

            cookies: list[CookieEditorCookie] = json.load(f)

            for cookie in cookies:
                self.browser.add_cookie({
                    "name": cookie['name'],
                    "value": cookie['value'],
                    "path": cookie['path'],
                    "secure": cookie['secure'],
                    "sameSite": sameSiteTranslator.get(cookie['sameSite'], 'Strict'),
                    "httpOnly": cookie['httpOnly'],
                    "expire": cookie.get('expirationDate', None)
                })

        self.browser.get(self.HOME)

    def _wait_and_press_not_now(self):
        botao_not_now = "#tux-portal-container > div:nth-child(3) > div > div > div > div > div.TUXModal.TUXModal--width-Medium.TUXModal--height-undefined.TUXModal--entered > div.jsx-2037160096.content > div.jsx-2037160096.footer > button.css-1ypeuck"

        try:
            WebDriverWait(self.browser, timeout=20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, botao_not_now))
            )
        except:
            print("Not nao nao encontrado")

        botoes_not_now = self.browser.find_elements(By.CSS_SELECTOR, botao_not_now)
        if len(botoes_not_now) > 0:
            botao = botoes_not_now[0]
            botao.click()
            time.sleep(2)

    def post(self, video_paths: str|list[str], caption: str=''):
        if isinstance(video_paths, str):
            video_paths = [video_paths]
        
        self.browser.get(self.UPLOAD_URL)

        for video_path in video_paths:
            iframe: WebElement|None = None
            while True:
                try:
                    WebDriverWait(self.browser, 60).until(
                        EC.visibility_of_element_located(
                            (By.TAG_NAME, 'iframe')
                        )
                    )

                    time.sleep(5)

                    iframe = self.browser.find_element(
                        By.TAG_NAME,
                        'iframe'
                    )
                    break
                except NoSuchElementException:
                    pass
            
            self.browser.switch_to.frame(iframe)

            time.sleep(4)

            file_field = self.browser.find_element(
                by=By.CSS_SELECTOR,
                value=self.UPLOAD_INPUT_SELECTOR
            )
            file_field.send_keys(
                os.path.abspath(video_path)
            )

            WebDriverWait(self.browser, 60).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.notranslate'))
            )

            time.sleep(3)


            caption_field = self.browser.find_element(
                by=By.CSS_SELECTOR,
                value=".notranslate"
            )
            
            for caption_part in caption.split(" "):
                try:
                    caption_field.send_keys(caption_part)

                    if caption_part.startswith('#'):
                        time.sleep(1)
                        caption_field.send_keys(Keys.ARROW_DOWN)
                        caption_field.send_keys(Keys.ARROW_UP)
                        caption_field.send_keys(Keys.RETURN)
                    
                    caption_field.send_keys(' ')
                except:
                    self._wait_and_press_not_now()

            WebDriverWait(self.browser, timeout=300).until(
                EC.any_of(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-y1m958")),
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.NOT_NOW_BUTTON_SELECTOR))
                )
            )

            time.sleep(3)

            self._wait_and_press_not_now()

            try:
                self.browser.find_element(By.CSS_SELECTOR, ".css-y1m958").click()
            except:
                print("Não encontrei o botão :/")
                self._wait_and_press_not_now()
                
                try:
                    self.browser.find_element(By.CSS_SELECTOR, ".css-y1m958").click()
                except:
                    
                    print("Nao encontrou de novo...")
                    time.sleep(5)
                    self._wait_and_press_not_now()
                    time.sleep(5)

            WebDriverWait(self.browser, timeout=60).until(
                EC.visibility_of_element_located((
                    By.CSS_SELECTOR,
                    'div.tiktok-modal__modal-mask > div > div.tiktok-modal__modal-footer.is-horizontal > div.tiktok-modal__modal-button.is-highlight'
                ))
            )

            time.sleep(2)

            self.browser.find_element(
                By.CSS_SELECTOR,
                'div.tiktok-modal__modal-mask > div > div.tiktok-modal__modal-footer.is-horizontal > div.tiktok-modal__modal-button.is-highlight'
            ).click()

            self.browser.switch_to.parent_frame()

    def close(self):
        self.browser.close()
