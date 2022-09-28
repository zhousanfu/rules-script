#!python3.8
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2022-09-13 18:22:30
 LastEditors: Sanfor Chow
 LastEditTime: 2022-09-16 19:26:54
 FilePath: /rules_script/Qx&Loon/collect.py
'''
import os, re, json, time, requests
import hashlib
bast_path = os.getcwd()
data_path = bast_path + '/Qx&Loon/data'







class Resolver(object):
    def __init__(self, fileName):
        self.__fileName = fileName

    def Resolve(self):
        def match(pattern, string):
            matchObj = re.match(pattern, string)
            if matchObj:
                    #print(matchObj.group())
                    return True
            return False

        blockList = []
        unblockList = []
        if not os.path.exists(self.__fileName):
            return blockList,unblockList
        with open(self.__fileName, "r") as f:
            for line in f:
                # 去掉换行符
                line = line.replace('\r', '').replace('\n', '').strip()
                # 去掉空行
                if len(line) < 1:
                    continue
                # 跳过注释! #
                if match('^!.*', line) or match('^#.*', line):
                    continue
                # 跳过注释[]
                if line.find('[') == 0 and line.rfind(']')== len(line)-1:
                    continue
                # ||
                if match('^\|\|.*', line):
                    #print(line)
                    blockList.append(line)
                    continue
                # /REGEX/
                if match('^/.*', line):
                    #print(line)
                    blockList.append(line)
                    continue
                # @@
                if match('^@@.*', line):
                    #print(line)
                    unblockList.append(line)
                    continue

                # @ 注释
                if match('^@.*', line):
                    #print(line)
                    continue

                # host 模式
                if line.find('0.0.0.0')==0 or line.find('127.0.0.1') == 0:
                    row = line.split(' ')
                    row = list(map(lambda x: x.strip(), row)) # 字段去空格
                    for i in range(len(row)-1):
                        if len(row[i]) == 0:
                            row.pop(i)
                    domain = row[1]
                    if domain in ['localhost', 'localhost.localdomain', 'local', '0.0.0.0']:
                        continue
                    domain = '||%s^'%(domain)
                    blockList.append(domain)
                    continue

                # 过滤无效的hosts
                if line.replace(' ', '') in ['::1localhost','255.255.255.255broadcasthost','::1ip6-localhost','::1ip6-loopback','fe80::1%lo0localhost','ff00::0ip6-localnet','ff00::0ip6-mcastprefix','ff02::1ip6-allnodes','ff02::2ip6-allrouters','ff02::3ip6-allhosts','255.255.255.255\tbroadcasthost']:
                    continue

                blockList.append(line)
                pass
        return blockList,unblockList        






if __name__ == '__main__':
    # url_list = ["https://easylist-downloads.adblockplus.org/easylistchina+easylistchina_compliance+easylist.txt",
    #             "https://easylist-downloads.adblockplus.org/easylist.txt",
    #             "https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt",
    #             "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rewrite/Loon/AdvertisingLite/AdvertisingLite.plugin",
    #             ]
    # rules = get_rules(url_list)
    # make_file(rules)

    bast_path = os.getcwd()
    data_path = bast_path + '/Qx&Loon/data'
    rule_data_path = data_path+'/rule_data.txt'

    # 下载-合并规则
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
    fw = open(rule_data_path, 'w')
    for i in data:
        fw.write(i+'\n')
    fw.close()

    # ruleList = GetRuleList(file)
    # isUpdate = False
    # lastUpdate = time.strftime("%Y/%m/%d", time.localtime())
    # for i in range(0, len(ruleList)):
    #     relue = Rule(ruleList[i][0], ruleList[i][1])
    #     if relue.Update():
    #         isUpdate = True
    #         ruleList[i][2] = lastUpdate
    # if isUpdate:
    #     blockList = []
    #     unblockList = []
    #     for i in range(0, len(ruleList)):
    #         resolver = Resolver(os.getcwd() + '/rules/' + ruleList[i][0].replace(' ', '_') + '.txt')
    #         L1, L2 = resolver.Resolve()
    #         blockList += L1
    #         unblockList += L2
    #     # 生成合并规则
    #     CreatFiters(blockList, unblockList, pwd + '/rules/adblockfilters.txt')
    #     # 更新README.md
    #     CreatReadme(ruleList, pwd + '/README.md')

    # pwd = os.getcwd()
    # file = pwd + '/rules/Hblock_Filters.txt'
    # resolver = Resolver(file)
    # blockList, unblockList = resolver.Resolve()
    # print('blockList: %s'%(len(blockList)))
    # print('unblockList: %s'%(len(unblockList)))

