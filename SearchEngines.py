"""
from bokeh.plotting import figure
from bokeh.embed import components


plot = figure()
plot.circle([1,2], [3,4])

script, div = components(plot)
print(script)
print(div)
http://www.google.com/search?
  start=0
  &num=10
  &q=red+sox
  &cr=countryCA
  &client=google-csbe
  &output=xml_no_dtd

"""

import argparse
import sys

import re
from urllib.parse import urlparse, parse_qs,unquote
from lxml.html import fromstring
from requests import get

class Search_Engines():
    def __init__(self, *args, **kwargs):
        super(Search_Engines, self).__init__()
        p_args = argparse.ArgumentParser(description='Search results from Google,Bing,DuckDuckGo')
        p_args.add_argument("-search", action='store', dest='s_string', help="Search string include special characters",
                            type=str)
        p_args.add_argument("-country", action='store', dest='country_code', help="Counrty code", type=str)
        args = p_args.parse_args()
        src = args.s_string
        if re.search("\w",src) or re.search("\W",src):
            src=str(src.strip())

        self.seGoogle(str(src),str(args.country_code).upper())
        self.seBing(str(src), str(args.country_code).upper())
        self.seDuckDuckGo(str(src), str(args.country_code).upper())

    def seGoogle(self, sr_str, c_code):
        try:
            self.dsc = [];self.dsc.clear()
            ccode = "country" + c_code
            search_lnk = "https://www.google.com/search?start=0&num=11&q=" + sr_str + "&cr=" + str(ccode)
            print()
            r_google = get(search_lnk)
            if r_google.status_code == 200:
                page = fromstring(r_google.text)
                print("Google Results:")
                print(search_lnk)
                for spn in page.cssselect(".s span"):
                    self.dsc.append(spn.text_content())
                for i in self.dsc:
                    if i == "":
                        self.dsc.remove(i)
                for i, result in enumerate(page.cssselect(".r a")):
                    url = result.get("href")
                    if url.startswith("/url?"):
                        url = parse_qs(urlparse(url).query)['q']
                    print(str(i) + "\tTitle: " + str(result.text_content()) + "\n\t\tURL: " + str(
                        url[0]) + "\n\t\tDesc: " + str(self.dsc[i - 1]))
        except:
            pass

    def seBing(self, sr_str, c_code):
        try:
            d = [];d.clear()
            search_lnk = 'https://www.bing.com/search?q=' + sr_str + "&cc=" + c_code + "&limit=10"
            print()
            r_bing = get(search_lnk)
            if r_bing.status_code == 200:
                page = fromstring(r_bing.text)
                print("Bing Search: ")
                print(search_lnk)
                for dsc in page.cssselect(".b_caption p"):
                    d.append(dsc.text_content())
                for i, result in enumerate(page.cssselect(".b_algo h2 a")):
                    url = result.get("href")
                    if url.startswith("/url?"):
                        url = parse_qs(urlparse(url).query)['q']
                    print(str(i + 1) + "\tTitle: " + str(
                        result.text_content()) + "\n\t\tURL: " + url + "\n\t\tDesc: " + str(d[i - 1]))
        except:
            pass

    def seDuckDuckGo(self, sr_str, c_code):
        try:
            ccode = c_code.lower()
            dsc= []
            dsc.clear()
            cc = ['xa-ar', 'xa-en', 'ar-es', 'au-en', 'at-de', 'be-fr', 'be-nl', 'br-pt', 'bg-bg', 'ca-en', 'ca-fr',
                  'ct-ca',
                  'cl-es', 'cn-zh', 'co-es', 'hr-hr', 'cz-cs', 'dk-da', 'ee-et', 'fi-fi', 'fr-fr', 'de-de', 'gr-el',
                  'hk-tzh', 'hu-hu', 'in-en', 'id-id', 'id-en', 'ie-en', 'il-he', 'it-it', 'jp-jp', 'kr-kr', 'lv-lv',
                  'lt-lt', 'xl-es', 'my-ms', 'my-en', 'mx-es', 'nl-nl', 'nz-en', 'no-no', 'pe-es', 'ph-en', 'ph-tl',
                  'pl-pl',
                  'pt-pt', 'ro-ro', 'ru-ru', 'sg-en', 'sk-sk', 'sl-sl', 'za-en', 'es-es', 'se-sv', 'ch-de', 'ch-fr',
                  'ch-it',
                  'tw-tzh', 'th-th', 'tr-tr', 'ua-uk', 'uk-en', 'us-en', 'ue-es', 've-es', 'vn-vi', 'wt-wt']
            for i in cc:
                lng = i.split("-")[0]
                if ccode == "en":
                    ccode = "wt-wt"
                    continue
                if re.fullmatch(ccode,str(lng)):
                    ccode=i
            #search_url = " https://duckduckgo.com/?format=json&pretty=1&ko=1&kd=1&kaf=1&q="+str(sr_str)+"&kl="+str(ccode)#format=json&ie=web&kaf=10&kg=g&kv=n&kp=-1&k1=-1pretty=1&skip_disambig=1"
            search_url= "https://duckduckgo.com/html/?&q="+str(sr_str)+"&kl="+str(ccode)
            r_ddg = get(search_url)
            print()
            if r_ddg.status_code==200:
                page=fromstring(r_ddg.content)
                print("DuckDuckGo Search: ")
                print(search_url)
                for d in page.cssselect("div#links div div .result__snippet"):
                    if not d=="":
                        dsc.append(d.text_content())

                for i, result in enumerate(page.cssselect("div#links div div h2 a.result__a")):
                    url = result.get("href")
                    if url.startswith("/url?"):
                        url = parse_qs(urlparse(url).query)['q']
                    print(str(i + 1) + "\tTitle: " + str(result.text_content())+"\n\t\tURL: " + str(unquote(url.split("=")[2]))+ "\n\t\tDesc: " + str(dsc[i]))
        except:
            pass


if __name__ == "__main__":
    Search_Engines(sys.argv[1:])
