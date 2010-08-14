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
    
    //login/sign up button switch
    $('.sign-up-link').click(function() {
      $('#login_button').hide();
      $('#register_button').fadeIn();
      $('.sign-up').hide();
      $('.log-in').show();
      return false;
    });

    $('.login-link').click(function() {
      $('#register_button').hide();
      $('#login_button').fadeIn();
      $('.sign-up').show();
      $('.log-in').hide()
      return false;
    });
    
});