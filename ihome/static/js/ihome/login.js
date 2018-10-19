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
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        $.ajax({
            url: '/user/login/',
            type: 'POST',
            data: {"mobile": mobile, "password": passwd},
            dataType: 'json',
            success: function(data){
                if(data.code == 200){
                    alert("登录成功");
                    location.href = '/index/';
                }
                if(data.code == 1001){
                    $("#mobile-err span").html("手机号未注册")
                    $("#mobile-err").show();
                }
                if(data.code == 1002){
                    $("#password-err span").html("密码错误")
                    $("#password-err").show();
                }
            },
            error: function(){
                alert("登录失败");
                window.location.reload();
            }
        });
    });
})