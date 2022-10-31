#!python3.8
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2022-09-16 15:57:24
 LastEditors: Sanfor Chow
 LastEditTime: 2022-10-31 16:17:58
 FilePath: /rules_script/Qx&Loon/test.py
'''
import os, re, json, time, requests
BAST_PATH = os.getcwd()
DATA_PATH = BAST_PATH + '/Qx&Loon/data'
# print('data path:{}'.format(DATA_PATH))



# 获取规则
def rule_get():
    urls = json.load(open(DATA_PATH+'/rule_url.json', 'r'))
    data = []
    for url in urls:
        for k,v in url.items():
            try:
                for u in requests.get(v).text.split('\n'):
                    data.append(u)
                print('====> 成功：{}'.format(v))
            except:
                print('====> 失败：{}'.format(v))
    fw = open(DATA_PATH+'/rule_data.txt', 'w')
    for i in data:
        fw.write(i+'\n')
    fw.close()

    return data


# 清洗规则
def rule_clean(data):
    '''
    '''
    re_domain = re.compile('([a-zA-Z\d+\-]{1,}?\.){1,5}(?:(?!js|gif|jpg|png|[x_\$\*/~]).)(aero|aliyu|art|asia|beer|bid|biz|club|com|coop|edu|fun|gov|idv|info|ink|int|kim|ltd|mil|mobi|museum|name|net|online|org|pro|pub|run|site|top|video|vip|work|xin|xxx|xyz|[a-zA-Z]{2,2})') # [.\w-]*(:\d{,8})?((?=/)|(?!/))(aero|aliyu|art|asia|beer|bid|biz|club|com|coop|edu|fun|gov|idv|info|ink|int|kim|ltd|mil|mobi|museum|name|net|online|org|pro|pub|run|site|top|video|vip|work|xin|xxx|xyz|[a-zA-Z]{2,2})
    domain = []
    ip_cidr = []
    url_regex = []
    domain_suffix = []
    domain_keyword = []
    for i in data:
        # if bool(re.search("[#\!*]", i)):
        #     pass
        # else:
        #     i = re.sub(r"(^[@|]*)", "", i)
        #     i = re.sub("\^", "", i)

        if bool(re.search(r'/ad[s]?(/|.)|(/|\.)/ad|(/|.)/ads|^[#\!*]', i)):
            pass
        else:
            if bool(re.search('DOMAIN-SUFFIX', i)):
                try:
                    i_split = re.search(re_domain, i).group()
                    domain_suffix.append(i_split)
                except:
                    i_split = i.split(',')
                    if len(i_split) == 1:
                        domain_suffix.append(i_split[0])
                    elif len(i_split) == 2:
                        domain_suffix.append(i_split[0])
                    elif len(i_split) >= 3:
                        domain_suffix.append(i_split[2])
            elif bool(re.search('DOMAIN-KEYWORD', i)):
                try:
                    i_split = re.search(re_domain, i).group()
                    domain_keyword.append(i_split)
                except:
                    i_split = i.split(',')
                    if len(i_split) == 1:
                        domain_keyword.append(i_split[0])
                    elif len(i_split) == 2:
                        domain_keyword.append(i_split[0])
                    elif len(i_split) >= 3:
                        domain_keyword.append(i_split[2])
            elif bool(re.search(re_domain, i)):
                i_split = re.search(re_domain, i).group()
                domain.append(i_split)
            elif bool(re.search('URL-REGEX', i)):
                i_split = i.split(',')
                if len(i_split) >= 2:
                    url_regex.append(i_split[1])
            elif bool(re.search('IP-CIDR', i)):
                i_split = i.split(',')
                if len(i_split) >= 2:
                    ip_cidr.append(i_split[1])

    # 规则合并写入、统计、分类
    domain = list(set(domain))
    ip_cidr = list(set(ip_cidr))
    url_regex = list(set(url_regex))
    domain_suffix = list(set(domain_suffix))
    domain_keyword = list(set(domain_keyword))

    return domain,ip_cidr,url_regex,domain_suffix,domain_keyword


# 生成合并规则
def rule_write(domain,ip_cidr,url_regex,domain_suffix,domain_keyword, path_name):
    fw = open(DATA_PATH+'/'+path_name+'domain.txt', 'w')
    urls = json.load(open(DATA_PATH+'/rule_url.json', 'r'))
    fw.write('# 各规则总量\n# DOMAIN:{}\n# DOMAIN-KEYWORD:{}\n# DOMAIN-SUFFIX:{}\n# IP-CIDR:{}\n# URL-REGEX:{}\n'.format(str(len(domain)), str(len(domain_suffix)), str(len(domain_keyword)), str(len(ip_cidr)), str(len(url_regex))))
    fw.write('# 来源：{}'.format(str(urls)))
    fw.write('\n\n\n')
    fw.write("# ==================== DOMAIN =====================STA"+'\n')
    try:
        domain = [i.split('.') for i in domain]
        domain.sort(key=lambda x:x[0])
    except:
        pass
    try:
        domain_keyword = [i.split('.') for i in domain_keyword]
        domain_keyword.sort(key=lambda x:x[0])
    except:
        pass
    try:
        domain_suffix = [i.split('.') for i in domain_suffix]
        domain_suffix.sort(key=lambda x:x[0])
    except:
        pass
    for i in domain:
        if bool(re.search(r'^[\-\+]', '.'.join(i))):
            pass
        else:
            fw.write("  - '"+ '.'.join(i) +"'"+"\n")
    # w.write("# ==================== DOMAIN =====================END"+'\n\n')
    # fw.write("# ==================== DOMAIN-KEYWORD =============STA"+'\n')
    fw.close()
    fw = open(DATA_PATH+'/'+path_name+'domain_keyword.txt', 'w')
    for i in domain_keyword:
        if bool(re.search(r'^[\-\+]', '.'.join(i))):
            pass
        else:
            fw.write('  - DOMAIN-KEYWORD,'+ '.'.join(i) +',REJECT'+'\n')
    # fw.write("# ==================== DOMAIN-KEYWORD =============END"+'\n\n')
    # fw.write("# ==================== DOMAIN-SUFFIX ==============STA"+'\n')
    fw.close()
    fw = open(DATA_PATH+'/'+path_name+'domain_suffix.txt', 'w')
    for i in domain_suffix:
        if bool(re.search(r'^[\-\+]', '.'.join(i))):
            pass
        else:
            fw.write('  - DOMAIN-SUFFIX,'+ '.'.join(i) +',REJECT'+'\n')
    # fw.write("# ==================== DOMAIN-SUFFIX ==============END"+'\n\n')
    fw.close()

    fw = open(DATA_PATH+'/'+path_name+'class.txt', 'w')
    urls = json.load(open(DATA_PATH+'/rule_url.json', 'r'))
    fw.write('# 各规则总量\n# DOMAIN:{}\n# DOMAIN-KEYWORD:{}\n# DOMAIN-SUFFIX:{}\n# IP-CIDR:{}\n# URL-REGEX:{}\n'.format(str(len(domain)), str(len(domain_suffix)), str(len(domain_keyword)), str(len(ip_cidr)), str(len(url_regex))))
    fw.write('# 来源：{}'.format(str(urls)))
    fw.write('\n\n\n')


    try:
        url_regex = [i.split('.') for i in url_regex]
        url_regex.sort(key=lambda x:x[0])
    except:
        pass
    try:
        ip_cidr = [i.split('.') for i in ip_cidr]
        ip_cidr.sort(key=lambda x:x[0])
    except:
        pass
    # fw.write("# ==================== IP-CIDR ====================STA"+'\n')
    for i in ip_cidr:
        if bool(re.search(r'^[\-\+]|#', '.'.join(i))):
            pass
        else:
            fw.write('  - IP-CIDR,'+ '.'.join(i) +',no-resolve'+'\n')
    # fw.write("# ==================== IP-CIDR  ===================END"+'\n\n')
    # fw.write("# ==================== URL-REGEX ==================STA"+'\n')
    # for i in url_regex:
    #     if bool(re.search(r'^[\-\+]|#', '.'.join(i))):
    #         pass
    #     else:
    #         fw.write('  - URL-REGEX,'+ '.'.join(i) +'\n')
    # fw.write("# ==================== URL-REGEX ==================END"+'\n\n')



if __name__=="__main__":
    # rule_get()
    # data = requests.get('https://easylist-downloads.adblockplus.org/easylistchina+easylistchina_compliance+easylist.txt').text.split('\n')
    # fw = open(DATA_PATH+'/easylist.txt', 'w')
    # for i in data:
    #     fw.write(i+'\n')
    # fw.close()

    data = open(DATA_PATH+'/rule_data.txt', 'r').read().split('\n')
    domain,ip_cidr,url_regex,domain_suffix,domain_keyword = rule_clean(data)
    rule_write(domain,ip_cidr,url_regex,domain_suffix,domain_keyword, path_name='ads_')