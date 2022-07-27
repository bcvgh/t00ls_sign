import json
import requests
import bs4
import re
requests.packages.urllib3.disable_warnings()
username = '***********'  # 帐号
password = '******************'  # 密码MD5 32位(小写)
question_num = '*'  # 安全提问 参考下面
question_answer = '**'  # 安全提问答案
proxies = {
    'https': "http://127.0.0.1:8080",
    'http': "http://127.0.0.1:8080"
}
headers = {
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
             "Accept":"*/*",
             "Accept-Encoding":"gzip,deflate",
             "Connection":"close",
             "Content-Type":"application/x-www-form-urlencoded"
             }

def t00ls_login(u_name, u_pass, q_num, q_ans):
    login_data = {
        'username': u_name,
        'password': u_pass,
        'questionid': q_num,
        'answer': q_ans,
        'cookietime': 2592000,
        'loginsubmit':'登录',
        'redirect':'https://www.t00ls.com'
    }
    response_login = requests.post('https://www.t00ls.com/login.html', proxies=proxies, verify=False, headers=headers)
    soup = bs4.BeautifulSoup(response_login.text, 'lxml')
    # if response_login_json['status'] != 'success':
    #     return None
    if response_login.status_code != 302:
        formhash = soup.find_all("input")[5].attrs["value"]
        formhash1 = {"formhash": formhash}
        login_data.update(formhash1)
        response_login1 = requests.post(url='https://www.t00ls.com/login.html', data=login_data, headers=headers,
                                        verify=False, proxies=proxies,)
        if response_login1.history[0].status_code == 302:
            cookie_value = requests.utils.dict_from_cookiejar(response_login1.history[0].cookies)

            # t00ls_cookies = response_login1.history[0].cookies.items()
            # cookie_value = ''
            # for key, value in t00ls_cookies:
            #     cookie_value += key+'='+value+';'
            # return formhash, cookie_value
            return formhash, cookie_value
        else:
            return None
    # else:
    #     print('用户:', username, '登入成功!')
    #     formhash = response_login_json['formhash']
    #     t00ls_cookies = response_login.cookies
    #     return formhash, t00ls_cookies


def t00ls_sign(t00ls_hash, t00ls_cookies):
    sign_data = {
        'formhash': t00ls_hash,
        'signsubmit': "apply"
    }
    # t00ls_cookies = {"Cookie": t00ls_cookies}
    # headers.update(t00ls_cookies)
    response_sign = requests.post('https://www.t00ls.com/ajax-sign.json', cookies=t00ls_cookies, data=sign_data,
                                  verify=False, proxies=proxies, headers=headers)
    soup = bs4.BeautifulSoup(response_sign.text, 'lxml')
    s=soup.find_all(href=re.compile("formhash"))
    pattern=re.compile('[0-9a-zA-Z]{8}')
    formhash = {"formhash": pattern.findall(str(s[0]))[1]}
    sign_data.update(formhash)
    response_sign = requests.post('https://www.t00ls.com/ajax-sign.json', cookies=t00ls_cookies, data=sign_data, verify=False, proxies=proxies, headers=headers)
    return json.loads(response_sign.text)


def main():
    response_login = t00ls_login(username, password, question_num, question_answer)
    if response_login:
        response_sign = t00ls_sign(response_login[0], response_login[1])
        if response_sign['status'] == 'success':
            print('签到成功')
        elif response_sign['message'] == 'alreadysign':
            print('今日已签到')
        else:
            print('出现玄学问题了 签到失败')
    else:
        print('登入失败 请检查输入资料是否正确')


if __name__ == '__main__':
    main()