$(document).ready(function(){
    // 对发布房源，只有认证的用户才可以，所以需要先判断用户用户的实名认证状态
    $.get("/api/v1.0/users/auth", function (resp) {
        if (resp.errno === "4101") {
            // 用户未登录
            location.href = "/login.html";
        } else if (resp.errno === "0") {
            // 判断用户是否实名认证，未认证的去实名认证
            if (!(resp.data.real_name && resp.data.id_card)) {
                $(".auth-warn").show();
                return;
            }
            // 已经认证的用户，请求之前发布的房源信息
            $.get("/api/v1.0/user/houses", function (resp) {
                if (resp.errno === "0") {
                    $("#houses-list").html(template("houses-list-tmpl", {houses:resp.data.houses}));
                } else {
                    ("#houses-list").html(template("houses-list-tmpl", {houses:[]}));
                }

            });
        }
    });
})