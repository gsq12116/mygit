function logout() {
    $.get("/user/logout", function(data){
        if (data.code == 200) {
            location.href = "/user/login/";
        }
    });
}

$(document).ready(function(){
    $.get("/user/my_info/", function(data){
        if (data.code == 200){
            $("#user-name").html(data.name);
            $("#user-mobile").html(data.phone);
            $("#user-avatar").attr("src", "/static/media/"+data.avatar)
        }
    });

    })