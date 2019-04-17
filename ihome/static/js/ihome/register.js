function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
    // 形成图片验证码的后端地址，设置到页面中，让浏览器请求验证码图片
    // 1. 生成图片验证码的编号
    imageCodeId = generateUUID();
    // 设置图片url
    var url = "api/v1.0/image_codes/" + imageCodeId;
    $(".image-code img").attr("src", url);
}

function sendSMSCode() {
    // 点击发送短信验证码被执行函数
    // console.log("开始执行发送短信函数...");
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    // 构建后端请求参数
    var req_data = {
        image_code: imageCode, //图片验证码值
        image_code_id: imageCodeId //图片验证码的编号，全局变量
    };

    // 像后端发送请求
    $.get("/api/v1.0/sms_codes/"+ mobile, req_data, function(resp){
        // resp是后端返回的响应值，因为后端返回的是json字符串，
        // 所以Ajax帮助把json字符串转换为js对象，resp就是转换后对象
        // console.log("开始执行Ajax函数...");
        if (resp.errno == "0"){
            // 表示发送成功
            var num = 60;
            var timer = setInterval(function(){
                if (num >= 1){
                    // 修改倒计时文本
                    $(".phonecode-a").html(num + "秒");
                    num -= 1;
                }else {
                    // 恢复验证码字符，定时器和时间
                    $(".phonecode-a").html("获取验证码");
                    $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    clearInterval(timer);
                }
            }, 1000, 60)
        }else {
            console.log(resp.errmsg);
            alert(resp.errmsg);
            $(".phonecode-a").attr("onclick", "sendSMSCode();");
        }
    });


//     $.get("/api/smscode", {mobile:mobile, code:imageCode, codeId:imageCodeId},
//         function(data){
//             if (0 != data.errno) {
//                 $("#image-code-err span").html(data.errmsg);
//                 $("#image-code-err").show();
//                 if (2 == data.errno || 3 == data.errno) {
//                     generateImageCode();
//                 }
//                 $(".phonecode-a").attr("onclick", "sendSMSCode();");
//             }
//             else {
//                 var $time = $(".phonecode-a");
//                 var duration = 60;
//                 var intervalid = setInterval(function(){
//                     $time.html(duration + "秒");
//                     if(duration === 1){
//                         clearInterval(intervalid);
//                         $time.html('获取验证码');
//                         $(".phonecode-a").attr("onclick", "sendSMSCode();");
//                     }
//                     duration = duration - 1;
//                 }, 1000, 60);
//             }
//     }, 'json');
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
    $(".form-register").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        phoneCode = $("#phonecode").val();
        passwd = $("#password").val();
        passwd2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!phoneCode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }
    });
})