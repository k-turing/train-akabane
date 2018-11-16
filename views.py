# slack bot + Django + herokuで動くコードです。(赤羽に発着の電車限定)
# Django の views.pyにコピペしてください。

# requirements.txtに以下のコードを追加してください。
# beautifulsoup4==4.6.3
# bottle==0.12.13
# bs4==0.0.1
# lxml==4.2.5

# herokuを使用する場合は適時、上記のbs4などをimportしてください。


# コマンドを打って、電車の遅延状況を表示

from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
import json

# 使用する際は以下のコメントアウトを外してください
# from .models import Reply

# add extra module from here
import urllib.request
from bs4 import BeautifulSoup as bsp

VERIFICATION_TOKEN = 'neJbtCNAIf3PIC3YfVTAxbTz'
CALLBACK_WHICH_TRAIN = 'which train?'

# yahoo乗換案内からbs4を使ってスクレイピング

# 以下 reply
@csrf_exempt
def reply(request):
    if request.method != 'POST':
        return JsonResponse({})

    payload = json.loads(request.POST.get('payload'))
    if payload.get('token') != VERIFICATION_TOKEN:
        raise SuspiciousOperation('Invalid request.')

    if payload.get('callback_id') != CALLBACK_WHICH_TRAIN:
        raise SuspiciousOperation('Invalid request.')

    selected_value = payload['actions'][0]['selected_options'][0]['value']

    # 分岐はこれから短くします

    if selected_value == 'yamanote':
        html = urllib.request.urlopen('https://transit.yahoo.co.jp/traininfo/detail/21/0/').read()
        soup = bsp(html, 'lxml')

        information_element = soup.find('div', {'id': 'mdServiceStatus'})
        information = information_element.find('p').find(text = True, recursive = False)

        posting_date_element = information_element.find('p').find('span')
        posting_date = ''

        result = {
        'text' : '山手線\n' + information + posting_date
        }

    elif selected_value == 'keihintouhoku':
        html = urllib.request.urlopen('https://transit.yahoo.co.jp/traininfo/detail/22/0/').read()
        soup = bsp(html, 'lxml')

        information_element = soup.find('div', {'id': 'mdServiceStatus'})
        information = information_element.find('p').find(text = True, recursive = False)

        posting_date_element = information_element.find('p').find('span')
        posting_date = ''

        result = {
        'text' : '京浜東北根岸線\n' + information + posting_date
        }

    elif selected_value == 'shounan':
        html = urllib.request.urlopen('https://transit.yahoo.co.jp/traininfo/detail/25/0/').read()
        soup = bsp(html, 'lxml')

        information_element = soup.find('div', {'id': 'mdServiceStatus'})
        information = information_element.find('p').find(text = True, recursive = False)

        posting_date_element = information_element.find('p').find('span')
        posting_date = ''

        result = {
        'text' : '湘南新宿ライン[東京～熱海]\n' + information + posting_date
        }

    elif selected_value == 'toukaidou':
        html = urllib.request.urlopen('https://transit.yahoo.co.jp/traininfo/detail/27/0/').read()
        soup = bsp(html, 'lxml')

        information_element = soup.find('div', {'id': 'mdServiceStatus'})
        information = information_element.find('p').find(text = True, recursive = False)

        posting_date_element = information_element.find('p').find('span')
        posting_date = ''

        result = {
        'text' : '東海道本線[東京～熱海]\n' + information + posting_date
        }

    elif selected_value == 'takasaki':
        html = urllib.request.urlopen('https://transit.yahoo.co.jp/traininfo/detail/48/0/').read()
        soup = bsp(html, 'lxml')

        information_element = soup.find('div', {'id': 'mdServiceStatus'})
        information = information_element.find('p').find(text = True, recursive = False)

        posting_date_element = information_element.find('p').find('span')
        posting_date = ''

        result = {
        'text' : '高崎線\n' + information + posting_date
        }

    elif selected_value == 'saikyou':
        html = urllib.request.urlopen('https://transit.yahoo.co.jp/traininfo/detail/50/0/').read()
        soup = bsp(html, 'lxml')

        information_element = soup.find('div', {'id': 'mdServiceStatus'})
        information = information_element.find('p').find(text = True, recursive = False)

        posting_date_element = information_element.find('p').find('span')
        posting_date = ''

        result = {
        'text' : '埼京川越線[大崎～川越]\n' + information + posting_date
        }

    elif selected_value == 'uenotokyo':
        html = urllib.request.urlopen('https://transit.yahoo.co.jp/traininfo/detail/627/0/').read()
        soup = bsp(html, 'lxml')

        information_element = soup.find('div', {'id': 'mdServiceStatus'})
        information = information_element.find('p').find(text = True, recursive = False)

        posting_date_element = information_element.find('p').find('span')
        posting_date = ''

        result = {
        'text' : '上野東京ライン\n' + information + posting_date
        }


    if posting_date_element is not None:
        posting_date = posting_date_element.find(text = True, recursive = False)

    return JsonResponse(result)

# 以下 index
@csrf_exempt
def index(request):
    yamanote_replies = Reply.objects.filter(response=Reply.YAMANOTE)
    keihintouhoku_replies = Reply.objects.filter(response=Reply.KEIHINTOUHOKU)
    shounan_replies = Reply.objects.filter(response=Reply.SHOUNAN)
    toukaidou_replies = Reply.objects.filter(response=Reply.TOUKAIDOU)
    takasaki_replies = Reply.objects.filter(response=Reply.TAKASAKI)
    saikyou_replies = Reply.objects.filter(response=Reply.SAIKYOU)
    uenotokyo_replies = Reply.objects.filter(response=Reply.UENOTOKYO)


    context = {
        'yamanote_replies': yamanote_replies,
        'keihintouhoku_replies': keihintouhoku_replies,
        'shounan_replies': shounan_replies,
        'uenotokyo_replies': uenotokyo_replies,
        'toukaidou_replies': toukaidou_replies,
        'takasaki_replies': takasaki_replies,
        'saikyou_replies': saikyou_replies,

    }
    return render(request, 'index.html', context)