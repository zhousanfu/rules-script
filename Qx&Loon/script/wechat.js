

/*
 * @Author: Sanfor Chow
 * @Date: 2022-09-08 15:27:05
 * @LastEditors: Sanfor Chow
 * @LastEditTime: 2022-09-08 15:27:05
 * @FilePath: /rules_script/QuantumultX&Loon/script/wechat.js
 */
/*
微信 去除公众号文章底部广告

***************************
QuantumultX:

[rewrite_local]
^https?:\/\/mp\.weixin\.qq\.com\/mp\/getappmsgad url script-response-body https://raw.githubusercontent.com/NobyDa/Script/master/QuantumultX/File/Wechat.js

[mitm]
hostname = mp.weixin.qq.com

***************************
Surge4 or Loon:

[Script]
http-response ^https?:\/\/mp\.weixin\.qq\.com\/mp\/getappmsgad requires-body=1,max-size=0,script-path=https://raw.githubusercontent.com/NobyDa/Script/master/QuantumultX/File/Wechat.js

[MITM]
hostname = mp.weixin.qq.com

**************************/

var obj = JSON.parse($response.body);
obj.advertisement_num = 0;
obj.advertisement_info = [];
delete obj.appid;
$done({ body: JSON.stringify(obj) }); 