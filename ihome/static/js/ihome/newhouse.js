function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // 像后端获取城区数据
    $.get("/api/v1.0/areas", function (resp) {
        if (resp.errno === "0") {
            var areas = resp.data;
            for (i=0; i<areas.length; i++) {
                var area = areas[i];
                $("#area-id").append('<option value="'+ area.aid +'">'+ area.aname +'</option>');
            }

            // 使用js模板
            var html = template("areas-tmpl", {areas: areas})
            $("#area-id").html(html);
        } else {
            alert(resp.errmsg);
        }


    })

    $("#form-house-info").submit(function (e) {
        e.preventDefault();

        // 处理表单提交的数据
        var data = {};
        $("#form-house-info").serializeArray().map(function (x) { data[x.name]=x.value });

        // 收集设置的id信息
        var facility = [];
        $(":checked[name=facility]").each(function (index, x) {
            facilty[index] = $(x).val()
        });
        data.facility = facility;

        // 像后端发送请求
        $.ajax({
            url: "/api/v1.0/houses/info",
            type: "post",
            contenType: "application/json",
            data: JSON.stringify(data),
            dataType: "json",
            hraders: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno === "4101") {
                    // 用户未登录
                    loaction.href = "/login.html";
                } else if (resp.errno === "0") {
                    // 隐藏基本信息表单
                    $("#form-house-info").hide();
                    // 显示图片表单
                    $("#form-house-image").show();
                    // 设置图片表单中的house_id
                    $("#house-id").val(resp.data.house_id);
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    });

    // 提交房屋照片
    $("#form-house-image").submit(function (e) {
        e.preventDefault(); // 阻止表单默认提交行为

        // 因为不知道提交数据（图片）的类型，所以使用ajaxSubmit方法，进行数据的提交
        $(this).ajaxSubmit({
            url: "/api/v1.0/houses/image",
            type: "post",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token"),
            },
            success: function (resp) {
                if (resp.errno === "4101") {
                    loaction.href = "/login.html";
                } else if (resp.errno === "0") {
                    $(".house-image-cons").append('<img src="'+ resp.data.image_url'">');
                } else {
                    alert(resp.errmsg);
                }
            }


        })
    })
});


