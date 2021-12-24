
const $ = new Env('太太乐');
var request = require("request");
let status;
status = (status = ($.getval("ttlstatus") || "1") ) > 1 ? `${status}` : ""; // 账号扩展字符
let ttlhdArr = [],ttlcount = ''
let ttlhd= $.isNode() ? (process.env.ttlhd ? process.env.ttlhd : "") : ($.getdata('ttlhd') ? $.getdata('ttlhd') : "")

let ttlhds = ""
const logs =0;
const host='https://www.ttljf.com/ttl_chefHub/'
var hours = new Date().getHours();
var s = new Date().getMinutes();

var timestamp = Math.round(new Date().getTime()/1000).toString();
!(async () => {
  if (typeof $request !== "undefined") {
        await ttlck()
  } else {
      if(!$.isNode()){
          ttlhdArr.push($.getdata('ttlhd'))
          let ttlcount = ($.getval('ttlcount') || '1');
          for (let i = 2; i <= ttlcount; i++) {
            ttlhdArr.push($.getdata(`ttlhd${i}`))
            }
    console.log(`------------- 共${ttlhdArr.length}个账号-------------\n`)
      for (let i = 0; i < ttlhdArr.length; i++) {
        if (ttlhdArr[i]) {
          ttlhd = ttlhdArr[i];
          $.index = i + 1;
        
          console.log(`\n开始【太太乐${$.index}】`)
          console.log(`第一次注册必须先登录一次小程序绑定微信然后用接口\n不会抓包的手残智力障碍的接口获取token\nhttp://47.101.146.160/ttl.php?zh=手机号码&mm=密码\n如需换话费 下载太太乐APP积分兑换话费\n如果没库存了 自己隔天再看`)
         
await sign()
await blog()
await my() 
  }
}
      }else  {
          if (process.env.ttlhd && process.env.ttlhd.indexOf('@') > -1) {
            ttlhdArr = process.env.ttlhd.split('@');
            console.log(`您选择的是用"@"隔开\n`)
        } else {
            ttlhds = [process.env.ttlhd]
        };
        Object.keys(ttlhds).forEach((item) => {
        if (ttlhds[item]) {
            ttlhdArr.push(ttlhds[item])
        }
    })
          console.log(`共${ttlhdArr.length}个cookie`)
	        for (let k = 0; k < ttlhdArr.length; k++) {
                $.message = ""
                ttlhd = ttlhdArr[k]
                $.index = k + 1;
 
          console.log(`\n开始【太太乐${$.index}】`)
          console.log(`第一次注册必须先登录一次小程序绑定微信然后用接口\n不会抓包的手残智力障碍的接口获取token\nhttp://47.101.146.160/ttl.php?zh=手机号码&mm=密码\n如需换话费 下载太太乐APP积分兑换话费\n如果没库存了 自己隔天再看`)
          await kcjk(633)
          await kcjk(631)
          await kcjk(62)
          await kcjk(61)
await sign()
await blog()
await my() 
}


      }
  }
})()
  .catch((e) => $.logErr(e))
  .finally(() => $.done())


function ttlck() {
   if ($request.url.indexOf("user") > -1) {
  const ttlhd = $request.url

if(ttlhd)    $.setdata(ttlhd,`ttlhd${status}`)


$.log(ttlhd)
ttlhd = ttlhd.match(/loginToken=(.*?)&/)[1] 
$.log(ttlhd)
   $.msg($.name,"",'太太乐'+`${status}` +'数据获取成功！')
 
}
}
async function kcjk(giftId){
 return new Promise((resolve) => {
     
 let nm = {
   		url: `https://www.ttljf.com/ttl_site/giftApi.do?giftId=${giftId}&mthd=giftDetail&sign=569aeaef6da7470ae38e4907aab980da&userId=`,
   		headers:{
   		    'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
   		    
   		}
}
   $.get(nm,async(error, response, data) =>{
 
    try{
   aa = data.match(/{"code":"0000","message":"成功","url":".*","gifts":{"brand":"","collectId":0,"description":"/)      
   bb= data.match(/","exchangeLimit":.+/)     
        cc=aa+bb

         
        const result = JSON.parse(cc)
         $.msg(`${result.gifts.giftName} 需要积分：${result.gifts.price} 库存：${result.gifts.stockAmount}`)
       //$.log(`${result.gifts.giftName} 需要积分：${result.gifts.price} 库存：${result.gifts.stockAmount}`)
}catch(e) {
          $.logErr(e, response);
      } finally {
        resolve();
      } 
    })
   })
  }
