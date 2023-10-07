###############
# @Author: 6yy66yy
# @Date: 2021-07-26 16:44:05
# @LastEditors: 6yy66yy
# @LastEditTime: 2023-03-05 19:35:49
# @FilePath: \legod-auto-pause\legod.py
# @Description: 雷神加速器时长自动暂停，暂停程序，可以独立运行。
###############
import requests
import json
import os
import time
import hashlib #md5 加密
from typing import Union

class legod(object):
    def __init__(self):
        self.version = "v2.2.1-docker"
        self.pause_url='https://webapi.leigod.com/api/user/pause'
        self.info_url = 'https://webapi.leigod.com/api/user/info'
        self.login_url = 'https://webapi.leigod.com/api/auth/login'
        self.header = {
                # ':authority': 'webapi.nn.com',
                # ':method':'POST',
                # ':path':'/api/user/pause',
                # ':scheme': 'https',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.53',
                'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
                'Connection':"keep-alive",
                'Accept': "application/json, text/javascript, */*; q=0.01",
                'Accept-Encoding': "gzip, deflate, br",
                'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                'DNT': "1",
                'Referer': 'https://www.legod.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site'
                        }
        self.stopp=False
        self.conf=self.load()
        print('''
                ***************************************************
                *                                                 *
                *                                                 *
                *              雷神加速器自动暂停工具-DOCKER版本   *
                *                  当前版本：%s         *
                *                   作者: QuietBlade               *
                *                   感谢: 6yy66yy                  *
                *                                                 *
                *                                                 *
                *************************************************** '''%self.version)
    
    # 加载配置
    def load(self) -> tuple:
        '''
        加载配置文件

            文件名:configfile(在文件头定义,默认为config.ini)

        Returns:
            conf元组
        '''
        
        self.conf = {
            "uname": os.environ.get('UNAME', ''),        # 用户名/手机号
            "password": os.environ.get('PASSWD', ''),    # 密码(支持明文和md5)
            "account_token": os.environ.get('ACCOUNT_TOKEN', ''), # 用户的token
            "webhook" : os.environ.get('WEBHOOK', '') # webhook 路径, 目前支持 bark
        }
        # print(self.conf)
        return self.conf

    # 工具类 md5加密
    def genearteMD5(self,password):
        '''
        创建md5对象
        '''
        # 已经md5加密过的密码
        if len(self.conf['password']) == 32:
            # print("密码已加密,无需再次加密")
            return password
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        password = hl.hexdigest()
        self.conf['password'] = password
        return password

    # 登录
    def login(self):
        '''
        登录函数，当token无效的时候调用登录函数获取新的token

        Return:
            成功:True+新的token
            失败:False+错误信息
        '''
        uname = self.conf['uname']
        password = self.conf['password']
        if(uname=="" or password==""):
            return False
        token=""
        body={
            'username':uname,
            'password':self.genearteMD5(password),
            'user_type':'0',
            'src_channel':'guanwang',
            'country_code':86,
            'lang':'zh_CN',
            'region_code':1,
            'account_token':'null'
        }
        r = requests.post(self.login_url,data=body,headers = self.header)
        msg=json.loads(r.text)
        if(msg['code']==0):
            token = msg['data']['login_info']['account_token']
            self.conf['account_token'] = token
            return True,token
        else:
            print(msg['msg'])
            self.push(msg['msg'])
            raise Exception('请检查登录信息！')
            return False,msg['msg']
    
    #获取用户token
    def get_token(self) -> tuple:
        if len(self.conf["account_token"]) == 0:
            self.login()
        return self.conf["account_token"]

    # 获取用户信息
    def get_account_info(self,status : int = 2) -> tuple:
        '''
        获取账号信息
        Returns
        --------
        :class:`tuple`
            (True,账号信息) or (False,错误信息)
        '''
        if status == 0:
            return False, '用户名或密码错误导致无法获取账号信息'

        payload = {
            "account_token": self.get_token(),
            "lang":"zh_CN"
        }
        result = requests.post(self.info_url,data=payload,headers = self.header)
        msg = json.loads(result.text)
        # token 失效, 就再试一次
        if msg['code'] == 400006:
            self.conf['account_token'] = ''
            print('token失效, 将在1分钟后重新尝试')
            time.sleep(60)
            return self.get_account_info(status - 1)
        elif msg['code'] == 0:
            return True,msg['data']
        else:
            return False,msg['msg']
    
    # 检查当前状态
    def check_stop_status(self) -> bool:
        '''
        通过账号信息判断是否暂停
        0:正常,1:暂停
        '''
        status=self.get_account_info()[1]['pause_status_id']
        if(status == 1):
            return True
        else:
            return False
        
    # 暂停时长
    def pause(self,status : int = 3) -> Union[bool, str]:
        '''
        暂停加速,调用官网api

        Returns:
            官网返回的信息
        '''
        # sessions=requests.session()
        # sessions.mount('https://webapi.nn.com', HTTP20Adapter())
        # r =sessions.post(url,data=payload,headers = header)
        if self.check_stop_status():
            print("已处于暂停状态")
            return False
        payload = {
            "account_token" : self.conf['account_token'],
            "lang" : "zh_CN"
            }
        result = requests.post(self.pause_url,data=payload,headers = self.header)
        data = json.loads(result.text)
        if result.status_code==403:
            print("未知错误，可能是请求频繁或者是网址更新, 将在10分钟后重试尝试")
            self.push("未知错误，可能是请求频繁或者是网址更新, 将在10分钟后重试尝试")
            self.login()
            return self.pause(status - 1)
        self.push("暂停" + data['msg'])
        return data['msg']

    # webhook推送, 目前只做了bark推送, 详情@ https://github.com/Finb/Bark
    def push(self,message : str) -> bool:
        url = self.conf['webhook']
        if len(url) == 0:
            return False
        
        if "api.day.app" in url:
            headers = {'Content-Type': 'application/json'}
            if url[-1]  == '/':
                url = url + message
            else:
                url = url + '/' + message
            response = requests.post(url = url, data = json.dumps(), headers = headers)
            if response.status_code == 200:
                print("Webhook sent successfully")
            else:
                print(f"Failed to send webhook. Error: {response.text}")
            return True
        elif "api.telegram.org" in url:
            url = url + message
            response = requests.get(url = url)
            if response.status_code == 200:
                print("Webhook sent successfully")
            else:
                print(f"Failed to send webhook. Error: {response.text}")
            