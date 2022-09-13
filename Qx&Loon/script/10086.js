

/*
 * @Author: Sanfor Chow
 * @Date: 2022-09-08 14:41:11
 * @LastEditors: Sanfor Chow
 * @LastEditTime: 2022-09-08 14:41:12
 * @FilePath: /rules_script/QuantumultX&Loon/js/10086.js
 */
/*
[mitm]
10086.online-cmcc.cn
[rewrite_local](注意路径）
#10086_remove_ad
https:\/\/10086\.online\-cmcc\.cn\:20010\/gfms\/front\/hn\/busi3\!getAdvert url script-response-body 10086.js
*/

let obj = JSON.parse($response.body);

obj.flag = 0;
obj.content = " ";

$done({ body: JSON.stringify(obj) })