// 获取cookie
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });

    // 为表单提交补充自定义函数行为
    $(".form-login").submit(function (e) {
        // 阻止浏览器默认的表单自动提交功能
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请输入正确的手机号！");
            $("#mobile-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请输入密码！");
            $("#password-err").show();
            return;
        }

        // Ajax请求跳转到首页
        var req_data = {
            mobile:mobile,
            password:passwd
        };

        // 将data转为json字符串
        var req_json = JSON.stringify(req_data);
        $.ajax({
            url: "/api/v1.0/sessions",
            type: "post",
            data: req_json,
            contentType: "application/json",
            dataType: "json",
            headers: {
                "x-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "0"){
                    //登录成功，跳转到主页
                    location.href = "/";
                }else {
                    $("#password-err span").html(resp.errmsg);
                    $("#password-err").show();
                }
            }

        });
    });
});


