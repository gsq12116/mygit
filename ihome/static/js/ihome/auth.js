function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}
$(document).ready(function(){
    $(".btn-success").hide();
    $.get("/user/id_info/", function(data){
        if (data.code == 200){
            $("#real-name").val(data.id_name);
            $("#real-name").attr("readonly", "readonly");
            $("#id-card").val(data.id_card);
            $("#id-card").attr("readonly", "readonly");
        }
        if (data.code == 2000){
            $(".btn-success").show();
        }
    });
    $("#form-auth").submit(function(e){
        e.preventDefault();
        $.ajax({
            url: '/user/id_info/',
            type: 'POST',
            data:{"id_name": $("#real-name").val(), "id_card": $("#id-card").val()},
            dataType: 'json',
            success: function(data){
                if(data.code == 200){
                    showSuccessMsg();
                    window.location.reload();
                }
                if(data.code == 2001){
                    alert("姓名格式错误，请填写正确的姓名");
                }
                if(data.code == 2002){
                    alert("身份证格式错误，请填写正确的身份证号码");
                }
                if(data.code == 2000){
                    $(".error-msg").css("display", "block");
                }
            },
            error: function(data){
                alert("请求失败");
            }
        });
    });
    $("input").focus(function(){
         $(".error-msg").css("display", "none");
    });
});



