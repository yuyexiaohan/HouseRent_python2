function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

// 匹配cookie值
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // 查询用户实名认证信息
    $.get("/api/v1.0/users/auth", function (resp) {
        // 4101代表用户未登录
        if (resp.errno === "4101") {
            loaction.href = "/login.html";
        } else if (resp.errno === "0") {
            // 如果返回的real_name与id_card不为null，表示用户已经填写实名认证信息，就在实名认证页面展示实名认证的信息
            if (resp.data.real && resp.data.id_card) {
                $("#real-name").val(resp.data.real_name);
                $("#id-card").val(resp.data.id_card);
                // 给input标签添加disabled属性，禁止用户修改数据
                $("#real-name").prop("disabled", true);
                $("#id-card").prop("disabled", true);
                // 并隐藏提交按钮
                $("#form-auth>input[type=submit]").hide();
            }
        } else {
            alert(resp.errmsg);
        }
    }, "json");

    // 管理实名信息表单提交功能
    $("#form-auth").submit(function (e) {
        e.preventDefault();
        // 获取前端用户填写信息
        var realName = $("#real-name").val();
        var idCard = $("#id-card").val();
        // 如果信息不完整，显示错误信息
        if (realName === "" || idCard === "") {
            $(".error-msg").show();
        }

        // 将表单的数据转换未json字符串
        var data = {
            real_name: realName,
            id_card: idCard
        };
        var jsonData = JSON.stringify(data);
        console.log("开始执行ajax");
        // ajax向后端提交数据
        $.ajax({
            url: "/api/v1.0/users/auth",
            type: "post",
            data: jsonData,
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno === "0") {
                    $(".error-msg").hide();
                    // 显示保存成功的提示信息
                    showSuccessMsg();
                    $("#real-name").prop("disabled", true);
                    $("#id-card").prop("disabled", true);
                    $("#form-auth>input[type=submit]").hide();

                }
            }
        });
    })
});
