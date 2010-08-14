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
    
    //login/sign up textifeld clearing
    var searchDefaultText = $("#id_email").attr("value");

    var searchDefaultText2 = $("#id_password").attr("value");

    $("#id_email").focus(function(){  
      if($(this).attr("value") == searchDefaultText) $(this).attr("value", "");  
    });  
    $("#id_email").blur(function(){  
       if($(this).attr("value") == "") $(this).attr("value", searchDefaultText);  
    });

    $("#id_password").focus(function(){  
      if($(this).attr("value") == searchDefaultText2) $(this).attr("value", "");  
    });  
    $("#id_password").blur(function(){  
       if($(this).attr("value") == "") $(this).attr("value", searchDefaultText2);  
    });
    
    //login/sign up button switch
    $('.sign-up-link').click(function() {
      $('#login_register_form').attr('action', '/_register/');
      $('#login_button').hide();
      $('#register_button').fadeIn();
      $('.sign-up').hide();
      $('.log-in').show();
      return false;
    });

    $('.login-link').click(function() {
      $('#login_register_form').attr('action', '/_login/');
      $('#register_button').hide();
      $('#login_button').fadeIn();
      $('.sign-up').show();
      $('.log-in').hide()
      return false;
    });
    
});