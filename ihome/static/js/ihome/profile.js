function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


// $(document).ready(function () {
    // $("#form-avatar").submit(function (e) {
    //     // 阻止表单默认行为
    //     e.preventDefault();
    //     // 利用jquery.from.min.js提供的ajaxSubmit对表单进行异步提交
    //     console.log("开始上传图片");
    //     $(this).ajaxSubmit({
    //         url: "/api/v1.0/users/avatar",
    //         type: "post",
    //         dataType: "json",
    //         headers: {"X-CSRFToken": getCookie("csrf_token")},
    //         success: function (resp) {
    //             if (resp.errno === "0") {
    //                 // 上传成功
    //                 var avatarUrl = resp.data.avatar_url;
    //                 $("#user-avatar").attr("src", avatarUrl);
    //                 console.log("上传图片成功");
    //             } else if (resp.errno === "4101") {
    //                 location.href = "/login.html";
    //             } else {
    //                 alert(resp.errmsg);
    //             }
    //         }
    //     })
    // });
//
//
//     // 在页面加载有后端查询用户信息
//     $.get("/api/v1.0/user", function (resp) {
//         // 如果用户未登录，返回登录界面
//         if (resp.errno === "4101") {
//             location.href = "/login.html";
//         }
//         // 如果查询到数据
//         else if (resp.errno === "0") {
//             $("#user-name").val(resp.data.name);
//             if (resp.data.avatar) {
//                 $("#user-avatar").attr("src", resp.data.avatar);
//             }
//         }
//     }, "json");
//
//
//     // 更新个人信息
//     $("#form-name").submit(function (e) {
//         e.preventDefault();
//         // 获取参数
//         var name = $("#user-name").val();
//
//         if (!name) {
//             alert("请填写用户姓名！");
//             return;
//         }
//         $.ajax({
//             url:"/api/v1.0/users/name",
//             type: "PUT",
//             data: JSON.stringify({name: name}),
//             dataType: "json",
//             headers:{
//                 "X-CSRFToken": getCookie("csrf_token")
//             },
//             success: function (resp) {
//                 if (resp.errno === "0") {
//                     $(".error-msg").hide();
//                     showSuccessMsg();
//                 } else if (resp.errno === "4001") {
//                     $(".error-msg").show();
//                 } else if (resp.errno === "4101") {
//                     location.href = "/login.html";
//                 }
//             }
//         });
//     })
// });


$(document).ready(function () {
    $("#form-avatar").submit(function (e) {
        // 阻止表单的默认行为
        e.preventDefault();
        // 利用jquery.form.min.js提供的ajaxSubmit对表单进行异步提交
        // ajaxSubmit方法是在表单数据类型不确定的情况看下，直接使用ajaxSubmit()方法提交Ajax请求，其中不用带参数
        $(this).ajaxSubmit({
        // $.ajax({
            url: "/api/v1.0/users/avatar",
            type: "post",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno === "0") {
                    // 上传成功
                    var avatarUrl = resp.data.avatar_url;
                    alert("avatarUrl");
                    $("#user-avatar").attr("src", avatarUrl);
                } else if (resp.errno === "4101") {
                    location.href = "/login.html";
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    });

    // 在页面加载是向后端查询用户的信息
    $.get("/api/v1.0/user", function(resp){
        // 用户未登录
        if ("4101" === resp.errno) {
            location.href = "/login.html";
        }
        // 查询到了用户的信息
        else if ("0" === resp.errno) {
            $("#user-name").val(resp.data.name);
            if (resp.data.avatar) {
                $("#user-avatar").attr("src", resp.data.avatar);
            }
        }
    }, "json");

     $("#form-name").submit(function(e){
        e.preventDefault();
        // 获取参数
        var name = $("#user-name").val();

        if (!name) {
            alert("请填写用户名！");
            return;
        }
        $.ajax({
            url:"/api/v1.0/users/name",
            type:"PUT",
            data: JSON.stringify({name: name}),
            contentType: "application/json",
            dataType: "json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success: function (resp) {
                if ("0" === resp.errno) {
                    $(".error-msg").hide();
                    showSuccessMsg();
                } else if ("4001" === resp.errno) {
                    $(".error-msg").show();
                } else if ("4101" === resp.errno) {
                    location.href = "/login.html";
                }
            }
        });
    })
})
