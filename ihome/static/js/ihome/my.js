function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 点击退出按钮时执行得到函数
function logout() {
    $.ajax({
       url: "api/v1.0/session",
       type: "delete",
       dataType: "json",
       headers: {
           "X-CSRFToken": getCookie("csrf_token")
       },
       success: function (resp) {
           if (resp.errno == "0") {
               location.href = "/";
           }
       }
    });
}

$(document).ready(function(){
    $.get("/api/v1.0/user", function (resp) {
        // 用户登录
       if (resp.erron == "4101") {
           location.href = "login.html";
       }
       // 查询到了用户信息
        else if (resp.erron == "0") {
           $("#user-name").html(resp.data.name);
           $("#user-mobile").html(resp.data.mobile);
           if (resp.data.avatar) {
               $("#user-avatar").attr("src", resp.data.avatar)
           }
       }
    }, "json");
})