$(function(){
    $("#user_delete").click(function(){
         if ( confirm('Are you sure you want to delete your account? All your entries will no longer be functional.' ) )
        $.ajax({type: "DELETE",
                url: "/_settings/",
                dataType: "html",
                success: function(data){
                    if (data == "success") { window.location = "/"; }
                }});
        return false;
    });
    
    //relative time script
    $(".timeago").timeago();
    
    // facebox
    $('a[rel*=facebox]').facebox();
    $("#bookmarklet").tipsy({gravity: 's'});
    $("#bookmarklet").click(function(){
        $.facebox("Please drag the bookmarklet into the bookmarklet bar!");
        return false;
    })
    
    // upon selecting the file fire off the request
    $('#upload_form input[type=file]').change(function(e){
        $(".droplet").hide();
        $(".droplet_spinner").show();
        $("#upload_form").ajaxSubmit({
            dataType:  'json',
            data: {html: true},
            iframe: true,
            url: '/file_upload/',
            success:   function(data) {
                $('#upload_form input[type=file]').val("");
                $('.droplet_spinner').hide();
                $('.droplet').show();
                // alert with facebox containing the short url
                $.facebox("<input type='text' class='upload-url .tk-chennai-slab' value='"+data.url+"'><br /> <a href='http://twitter.com/home/?status="+data.url+"'>Tweet this</a>");
                $('.upload-url').select();
                $(".empty_entries").remove();
                $('#short_stats tbody').prepend('<tr><td class="link"><a href="'+data.url+'">'+data.url+'</a></td><td class="full_url"><a href="'+data.long_url+'">'+data.long_url+'</a></td><td class="when timeago">just now</td><td class="hits">0</td><td class="delete"><a href="#" class="link_delete"><img src="/static/css/images/delete.gif"></a></td></tr>');
            }
        });
        return false;
    });
    
    // delete entry
    $(".link_delete").live('click', function(){
        var self=$(this);
        if ( confirm('Are you sure'))
        $.ajax({url: self.attr("href"),
                type: 'DELETE',
                success: function(){
                        self.parents('tr').remove();
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
      $('#register_button').show();
      $('.sign-up').hide();
      $('.log-in').show();
      return false;
    });

    $('.login-link').click(function() {
      $('#login_register_form').attr('action', '/_login/');
      $('#register_button').hide();
      $('#login_button').show();
      $('.sign-up').show();
      $('.log-in').hide()
      return false;
    });
    
    //some table crap
    $(".home table tbody tr").hover(
      function () {
        $(this).addClass("table-hover");
        $(".home table tbody tr:even td").removeClass("table-even");
      }, 
      function () {
        $(this).removeClass("table-hover");
        $(".home table tbody tr:even td").addClass("table-even");
      }
    );
    
    $(".home table tbody tr:even td").addClass("table-even");
    
});