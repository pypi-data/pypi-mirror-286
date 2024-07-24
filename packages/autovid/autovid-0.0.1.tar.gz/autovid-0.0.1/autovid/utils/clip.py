from selenium import webdriver
from selenium.webdriver.common.by import By
from gtts import gTTS
import shutil

class Clip:
    def __init__(self,audio_str="",img_src=""):
        self._audio_str = audio_str
        self._img_src = img_src
        self._audio_engine = 'gtts'
        self._selenium_wrapper = None

    def get_audio_str(self):
        return self._audio_str

    def change_audio_str(self,audio_str):
        self._audio_str = audio_str

    def _gen_audio(self,path):
        if self._audio_engine == 'gtts':
            aud = gTTS(text=self._audio_str, lang='en', slow=False, tld='ca')
            aud.save(path)
        elif self._audio_engine == 'tiktok':
            pass
        else:
            raise Exception('invalid audio engine')

    def _gen_img(self,path):
        if not self._selenium_wrapper:
            if not img_src:
                raise Exception("image not found at " + img_src)
            shutil.copy(self._img_src,path)

        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        driver.get(self._selenium_wrapper['url'])
        
        if self._selenium_wrapper['type'] == 'post':
            element = driver.find_element(by=By.CLASS_NAME, value='block')

        if self._selenium_wrapper['type'] == 'comment':
            element = driver.find_element(by=By.CSS_SELECTOR, value ="shreddit-comment")
        
        element.screenshot(path)

        driver.quit()