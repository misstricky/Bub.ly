$(function(){
    $("#user_delete").click(function(){
        $.ajax({type: "DELETE",
                url: "/_settings/",
                dataType: "html",
                success: function(data){
                    if (data == "success") { window.location = "/"; }
                }});
        return false;
    });
    
});