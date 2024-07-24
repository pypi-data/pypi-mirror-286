try:
    import requests,urllib3,os,httpx
    from colorama import init, Fore, Style
except:
    import os
    os.system("pip install colorama && requests && urllib3")
import json
from typing import Literal
from time import sleep
try:
    from bs4 import BeautifulSoup
    from requests import get
    import random,requests
except:os.system("pip install bs4")


def get_useragent():
    return random.choice(_useragent_list)


_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]


def _req(term, results, lang, start, proxies, timeout):
    resp = get(
        url="https://www.google.com/search",
        headers={
            "User-Agent": get_useragent()
        },
        params={
            "q": term,
            "num": results + 2,  # Prevents multiple requests
            "hl": lang,
            "start": start,
        },
        proxies=proxies,
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5):
    """Search the Google search engine"""

    escaped_term = term.replace(" ", "+")

    # Proxy
    proxies = None
    if proxy:
        if proxy.startswith("https"):
            proxies = {"https": proxy}
        else:
            proxies = {"http": proxy}

    # Fetch
    start = 0
    while start < num_results:
        # Send request
        resp = _req(escaped_term, num_results - start,
                    lang, start, proxies, timeout)

        # Parse
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", attrs={"class": "g"})
        for result in result_block:
            # Find link, title, description
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find(
                "div", {"style": "-webkit-line-clamp:2"})
            if description_box:
                description = description_box.text
                if link and title and description:
                    start += 1
                    if advanced:
                        yield SearchResult(link["href"], title.text, description)
                    else:
                        yield link["href"]
        sleep(sleep_interval)
import httpx
def get_mp3_links_with_title(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Unable to access {url}")
        return {}
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No Title'
    links = soup.find_all('a')
    mp3_links = [link.get('href') for link in links if link.get('href') and link.get('href').endswith('.mp3')]
    if not mp3_links==[]:
        try:
            return {
        'name': title,
        'url': mp3_links[0]}
        except:...

class Email:
    def __init__(
            self,
            To: str,
            text: str,
            Title: str,
            Token: str,
            Input: Literal['info', 'app', 'Login', 'support'] = 'info'
        ) -> None:
        self.To = To
        self.text = text
        self.Title = Title
        self.Input = Input
        self.Token = Token
    
    def Send(self):
        Data = {
            'email': self.To,
            'text': str(self.text),  # تبدیل به رشته اطمینان می‌دهد که همیشه رشته است
            'head': self.Title,
            'token': self.Token,
            'title': self.Input
        }
        
        url = 'https://api-free.ir/api2/email.php'
        response = requests.post(url, data=Data)
        pars = response.json()
        print(pars)
        
        if pars.get('ok', False):
            return {
                'state': 'ok',
                'code': 200
            }
        else:
            return False

class client():
    def __init__(self,token: None = None,welcom: None = True)-> None:
        self.token=token
        self.welcom=welcom
        if welcom:
            message = f"""\n
            {Style.BRIGHT}Welcome to our library codern 3.8.16 !
            {Fore.GREEN}Website Dev : {Fore.RED}api-free.ir"""
            print(message)
    def Upload_file(self,Path)-> any:
        req=requests.post(
            "https://api-free.ir/api2/upload.php",
            data={'token':self.token},
            files={"file":open(Path,'rb')},
            timeout=60
        ).json()['result']
        return req
class api():
    def search_music(text:str,result_count:None = 5):
        meta=search(text, num_results=result_count)
        meta=[result for result in meta]
        return [get_mp3_links_with_title(data) for data in meta]
    def create_voice(
            text:str,
            mod:Literal['FaridNeural', 'DilaraNeural'] = 'FaridNeural'
        ) -> None:
        request=urllib3.PoolManager()
        headers = {'Content-Type': 'application/json'}
        data={'text':text,'mod':mod}
        response=httpx.post(
            'https://api-free.ir/api/voice.php',
            data={'text':text,'mod':mod},
            timeout=60
        )
        if response.status_code == 200:
            response_data = response.json()
            if 'result' in response_data:
                return response_data['result']
    def create_image(
            text:str,
            version:Literal['3.5', '2.5','1.5','4'] = '3.5',
            choice : None = False):
            body = {'text': text,'v': version}
            request = urllib3.PoolManager()
            response = request.request(
            'POST',
            'https://api-free.ir/api/img.php',
            fields=body)
            if response.status == 200:
                response_data = json.loads(response.data.decode('utf-8'))
                if 'result' in response_data:
                    if not choice:
                        return response_data['result']
                    else : 
                        return random.choice(response_data['result'])
                
    def download_post_rubika(
            share_url:str,
            #return_choice:None = False
    ):
        body = {'url': share_url}
        request = urllib3.PoolManager()
        response = request.request(
            'POST',
            'https://api-free.ir/api/rubino-dl.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
            
    def download_story_rubika(
            username:str
    ):
        body = {'id': username}
        request = urllib3.PoolManager()
        response = request.request(
            'POST',
            'https://api-free.ir/api2/story_rubino.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
    def search_page_rubino(
            text:str
    ):
        body = {'user': text}
        request = urllib3.PoolManager()
        response = request.request(
            'GET',
            'https://api-free.ir/api/rubino-search.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
    def get_ip_me()->None:
        request = urllib3.PoolManager()
        response = request.request('GET','https://api-free.ir/api/ip.php')
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'ip' in response_data:
                    return response_data['ip']
    def get_info_ip(
            ip:any,

    ):
        body = {'ip': ip}
        request = urllib3.PoolManager()
        response = request.request(
            'GET',
            'https://api-free.ir/api/ips.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']
    def get_page_instagram(username):
        body = {'name': username}
        request = urllib3.PoolManager()
        response = request.request(
            'GET',
            'https://api-free.ir/api/insta.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'Result' in response_data:
                    return response_data['Result']
    def search_wikipedia(
            text:str,
            lang:None = "fa"
    ):
        body = {'text': text,'lang':lang}
        request = urllib3.PoolManager()
        response = request.request(
            'POST',
            'https://api-free.ir/api/wiki.php',
            fields=body)
        if response.status == 200:
            response_data = json.loads(response.data.decode('utf-8'))
            if 'result' in response_data:
                    return response_data['result']