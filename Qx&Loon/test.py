#!python3.8
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2022-09-16 15:57:24
 LastEditors: Sanfor Chow
 LastEditTime: 2022-09-27 19:56:24
 FilePath: /rules_script/Qx&Loon/test.py
'''
import os, re, json, time, requests
bast_path = os.getcwd()
data_path = bast_path + '/Qx&Loon/data'
# print('data path:{}'.format(data_path))



# 获取规则
def get_rule():
    urls = json.load(open(data_path+'/rule_url.json', 'r'))
    data = []
    for url in urls:
        for k,v in url.items():
            try:
                for u in requests.get(v).text.split('\n'):
                    data.append(u)
                print('====> 成功：{}'.format(v))
            except:
                print('====> 失败：{}'.format(v))
    fw = open(data_path+'/rule_data.txt', 'w')
    for i in data:
        fw.write(i+'\n')
    fw.close()

    return data



def rule_clean(data, path):
    '''
    '''
    domain = []
    ip_cidr = []
    url_regex = []
    domain_suffix = []
    domain_keyword = []
    for i in data:
        if bool(re.search("[#\!*]", i)):
            pass
        else:
            i = re.sub(r"(^[@|]*)", "", i)
            i = re.sub("\^", "", i)
            if bool(re.search('URL-REGEX|^\.(cn|com|top|pub|xin|net|xyz|us|ru|org).{2,}|http', i)):
                i_split = i.split(',')
                if len(i_split) == 1:
                    url_regex.append(i_split[0])
                elif len(i_split) == 2:
                    url_regex.append(i_split[0])
                elif len(i_split) >= 3:
                    url_regex.append(i_split[2])
            elif bool(re.search('DOMAIN-SUFFIX', i)):
                i_split = i.split(',')
                if len(i_split) == 1:
                    domain_suffix.append(i_split[0])
                elif len(i_split) == 2:
                    domain_suffix.append(i_split[0])
                elif len(i_split) >= 3:
                    domain_suffix.append(i_split[2])
            elif bool(re.search('\.(cn|com|top|pub|xin|net|xyz|us|ru|org)$|DOMAIN-KEYWORD', i)):
                i_split = i.split(',')
                if len(i_split) == 1:
                    domain_keyword.append(i_split[0])
                elif len(i_split) == 2:
                    domain_keyword.append(i_split[0])
                elif len(i_split) >= 3:
                    domain_keyword.append(i_split[2])
            elif bool(re.search('.*\.(cn|com|top|pub|xin|net|xyz|us|ru|org)$|DOMAIN', i)):
                i_split = i.split(',')
                if len(i_split) == 1:
                    domain.append(i_split[0])
                elif len(i_split) == 2:
                    domain.append(i_split[0])
                elif len(i_split) >= 3:
                    domain.append(i_split[2])
            elif bool(re.search('\d+.\d+.\+.\d+/\d+|IP-CIDR', i)):
                i_split = i.split(',')
                if len(i_split) == 1:
                    ip_cidr.append(i_split[0])
                elif len(i_split) == 2:
                    ip_cidr.append(i_split[0])
                elif len(i_split) >= 3:
                    ip_cidr.append(i_split[2])

    domain = list(set(domain))
    domain.sort()
    ip_cidr = list(set(ip_cidr))
    ip_cidr.sort()
    url_regex = list(set(url_regex))
    url_regex.sort()
    domain_suffix = list(set(domain_suffix))
    domain_suffix.sort()
    domain_keyword = list(set(domain_keyword))
    domain_keyword.sort()

    fw = open(path, 'w')
    urls = json.load(open(data_path+'/rule_url.json', 'r'))
    fw.write('# 各规则总量\n# DOMAIN:{}\n# DOMAIN-KEYWORD:{}\n# DOMAIN-SUFFIX:{}\n# IP-CIDR:{}\n# URL-REGEX:{}\n'.format(str(len(domain)), str(len(domain_suffix)), str(len(domain_keyword)), str(len(ip_cidr)), str(len(url_regex))))
    fw.write('# 来源：{}'.format(str(urls)))
    fw.write('\n\n\n')
    fw.write("# ==================== IP-CIDR ====================STA"+'\n')
    for i in list(set(ip_cidr)):
        if bool(re.search('IP-CIDR', i)):
            fw.write(i+'\n')
        else:
            fw.write('IP-CIDR,'+i+',REJECT'+'\n')
    fw.write("# ==================== IP-CIDR  ====================END"+'\n\n')
    fw.write("# ==================== URL-REGEX ====================STA"+'\n')
    for i in list(set(url_regex)):
        if bool(re.search('URL-REGEX', i)):
            fw.write(i+'\n')
        else:
            fw.write('URL-REGEX,'+i+',REJECT'+'\n')
    fw.write("# ==================== URL-REGEX ====================END"+'\n\n')
    fw.write("# ==================== DOMAIN-KEYWORD ====================STA"+'\n')
    for i in list(set(domain_suffix)):
        if bool(re.search('DOMAIN-KEYWORD', i)):
            fw.write(i+'\n')
        else:
            fw.write('DOMAIN-KEYWORD,'+i+',REJECT'+'\n')
    fw.write("# ==================== DOMAIN-KEYWORD ====================END"+'\n\n')
    fw.write("# ==================== DOMAIN-SUFFIX ====================STA"+'\n')
    for i in list(set(domain_keyword)):
        if bool(re.search('DOMAIN-SUFFIX', i)):
            fw.write(i+'\n')
        else:
            fw.write('DOMAIN-SUFFIX,'+i+',REJECT'+'\n')
    fw.write("# ==================== DOMAIN-SUFFIX ====================END"+'\n\n')
    fw.write("# ==================== DOMAIN ====================STA"+'\n')
    for i in list(set(domain)):
        if bool(re.search('DOMAIN', i)):
            fw.write(i+'\n')
        else:
            fw.write('DOMAIN,'+i+',REJECT'+'\n')
    fw.write("# ==================== DOMAIN ====================END"+'\n\n')


if __name__=="__main__":
    # get_rule()
    data = requests.get('https://raw.githubusercontent.com/VeleSila/yhosts/master/hosts').text.split('\n')
    fw = open(data_path+'/ad_rules_yhosts.txt', 'w')
    for i in data:
        fw.write(i+'\n')
    fw.close()
    data = open(data_path+'/ad_rules_yhosts.txt', 'r').read().split('\n')
    rule_clean(data, data_path+'/ads_rules.txt')