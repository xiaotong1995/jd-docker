# !/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
cron:  0 * * * * TimingCash.py
new Env('太太乐奖品监控');
'''
import requests, json, os, random, time, re
from datetime import datetime
import schedule

# 礼品代码
gift_list = ['61', '62', '631', '633']
# 导入账户
try:
    from ttl_json import accounts

    lists = accounts
except Exception as error:
    print(f'失败原因:{error}')
    lists = []


# 获取Token
def get_token(iphone, passw):
    url = 'https://www.ttljf.com/ttl_site/user.do'
    # randomn=random.randint(10000,99999)
    header = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.14(0x18000e2f) NetType/4G Language/zh_CN'
    }
    data = {
        'device_brand': 'apple',
        'device_model': 'iPhone11, 8',
        'device_uuid': f'FCE{random.randint(10000, 99999)} - 32ED - 4C1D - 97DB - 59FED8E9CC59',
        'device_version': '14.6',
        'mthd': 'login',
        'password': passw,
        'platform': 'ios',
        'sign': '47f675126adc115bc92fd6a1358028b9',
        'username': iphone
    }
    try:
        result = requests.post(url, data=data, headers=header,timeout=60).text
        token = json.loads(result)['user']['loginToken']
        userid = json.loads(result)['user']['userId']
        return token, userid
    except Exception as e:
        print(e)


# 定义任务头部
def head(token):
    headers = {
        'Host': 'www.ttljf.com',
        'Accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'token': token,
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.14(0x18000e2f) NetType/4G Language/zh_CN',
        'Referer': 'https://servicewechat.com/wxe9aa8f1c4a77ddf5/17/page-frame.html',
    }
    return headers


# 做任务 任务HOST
host = 'https://www.ttljf.com/ttl_chefHub/'


def ttlsign(token):
    header = head(token)
    url = f'{host}user/api/sign/today'
    try:
        result = requests.put(url, headers=header,timeout=120).text
        message = json.loads(result)['message']
    except:
        message='请求错误'
    print(message)
    return message


def ttlshare(token):
    header = head(token)
    url = f'{host}Common/share/A35D575F-C004-4717-AABC-ED9D1979C3FA/blog'

    body = {"id": "A35D575F-C004-4717-AABC-ED9D1979C3FA", "type": "blog"}
    try:
        result = requests.put(url, data=body, headers=header,timeout=120).text
        message = json.loads(result)['message']
    except:
        message='请求错误'
    print(message)
    return message


def ttl_userinfo(token):
    header = head(token)
    url = f'{host}user/api/my'
    try:
        result = requests.get(url, headers=header,timeout=120).text
        integral = json.loads(result)['data']['integral']
    except:
        integral='请求错误'
    print(f'当前积分：{integral}')
    return integral


# 兑换礼品
def get_gift(token, userid, iphone, giftid):
    url = f'https://www.ttljf.com/ttl_site/chargeApi.do?giftId={giftid}&loginToken={token}&method=charge&mobile={iphone}&sign=47f675126adc115bc92fd6a1358028b9&userId={userid}'
    header = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.14(0x18000e2f) NetType/4G Language/zh_CN'
    }
    try:
        result = requests.get(url, headers=header,timeout=120).text
        r = json.loads(result)
        message = r['message']
        
    except:
        message='请求错误'
    print(f'兑换：{message}')
    return message


# 获取剩余数量
def gift_count(giftid):
    url = f'https://www.ttljf.com/ttl_site/giftApi.do?giftId={giftid}&mthd=giftDetail&sign=1275eded3f5a2ddc5794d59d97e0a852&userId='
    header = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.14(0x18000e2f) NetType/4G Language/zh_CN'
    }
    try:
        result = requests.get(url, headers=header,timeout=120).text
        r = json.loads(result)
        count = r['gifts']['stockAmount']
        name = r['gifts']['giftName']
        print(name,count)
        return name, count
    except Exception as e :
        print(f'查询数量{e}')


def do_task_and_get_gift(token, comp, iphone, userid):
    global messagea
    sign_mess = ttlsign(token)
    time.sleep(random.randint(2, 5))
    share_mess = ttlshare(token)
    integral = ttl_userinfo(token)
    #print(sign_mess)
    #print(share_mess)
    #print(int(integral))
    try:
        if '移动' in comp and int(integral) >= 45:
            name, count = gift_count(631)
            if int(count) > 0:
                messagea = get_gift(token, userid, iphone, 631)
                if '成功' in messagea:
                    messagea='成功兑换30元'
                else:
                   messagea=messagea
            else:
                messagea='数量不足，跳过'
        elif '电信' in comp and int(integral) >= 15:
            name, count = gift_count(633)
            if int(count) > 0:
                messagea = get_gift(token, userid, iphone, 633)
                if '成功' in messagea:
                    messagea='成功兑换10元'
                else:
                   messagea=messagea
            else:
                messagea='数量不足，跳过'
        elif '联通' in comp and int(integral) >= 7:
            name, count = gift_count(62)
            if int(count) > 0:
                messagea = get_gift(token, userid, iphone, 62)
                if '成功' in messagea:
                    messagea='成功兑换5元'
                else:
                   messagea=messagea
            else:
                name, count = gift_count(61)
                if int(count) > 0:
                    messagea = get_gift(token, userid, iphone, 61)
                    if '成功' in messagea:
                        messagea='成功兑换2元'
                    else:
                       messagea=messagea
                else:
                    messagea='数量不足，跳过'
        else:
            messagea = '不满足兑换条件，跳过'
        return sign_mess, share_mess, integral,messagea
    except Exception as e:
        print(e)


def maina():
    global lists
    m = 1
    me = ''
    for each in lists:
        try:
            print('-'*20+f'当前执行第个{m}账户'+'-'*20)
            if  each['iphone'] != '' and each['passw'] != '' and each['comp'] != '':
                iphone = each['iphone']
                passw = each['passw']
                comp = each['comp']
                qq=each['qq']
                #print('2')
                token, userid = get_token(iphone, passw)
                #print('3')
                sign_mess, share_mess,integral, messagea = do_task_and_get_gift(token, comp, iphone, userid)
                #print('4')
                me += f'第{m}个账户{iphone}:\n每日签到：{sign_mess}\n分享任务：{share_mess}\n积分：{integral}\n兑换：{messagea}\n'
            elif not all(each.values()):
                pushplus_bot('太太乐', f"第{m}个账户{qq}:\n空账户\n状态:跳过\n")
            m += 1
        except Exception as e:
            print(e)
    print(me)
    send_qq('', me)


# 定义pushplus推送
def pushplus_bot(title, content):
    PUSH_PLUS_TOKEN = '9e3f47b7e9dc47c6b7d4966851fc597b'
    try:
        print("\n")
        if not PUSH_PLUS_TOKEN:
            print("PUSHPLUS服务的token未设置!!\n取消推送")
            return
        print("PUSHPLUS服务启动")
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": PUSH_PLUS_TOKEN,
            "title": title,
            "content": content
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, data=body, headers=headers).json()
        if response['code'] == 200:
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)
#QQ推送

def send_qq(qqgroup,mess):
    QQurl=f"http://127.0.0.1:6547/send_group_msg?group_id={qqgroup}&message={mess}"
    try:
        print("\n")
        if not QQurl:
            print("QQ服务的token未设置!!\n取消推送")
            return
        print("QQ服务启动")
        response = requests.get(url=QQurl).json()
        print(response)
        if response['status'] == 'ok':
            print('推送成功！')
        else:
            print('推送失败！')
    except Exception as e:
        print(e)

'''
if __name__ == '__main__':    
    maina()
'''
schedule.every().day.at("09:17").do(maina)
schedule.every().day.at("12:17").do(maina)
while True:
    print(datetime.now())
    schedule.run_pending()
    time.sleep(1800)
