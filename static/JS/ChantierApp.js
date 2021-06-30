(function ($) {
    $(function() {
        function getCookie(name) {
         var cookieValue = null;
         if (document.cookie && document.cookie != '') {
             var cookies = document.cookie.split(';');
             for (var i = 0; i < cookies.length; i++) {
                 var cookie = jQuery.trim(cookies[i]);
                 // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
         }
         return cookieValue;
        }

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        var csrftoken = getCookie('csrftoken');
        // Ensure jQuery AJAX calls set the CSRF header to prevent security errors
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $(".Time-Selector a").each(function (){
           $(this).click(function () {
               var data = $(this).children("data").attr('value');
               const jsonString = 'data=' + data;
               $.ajax({
                   type: "POST",
                   data: jsonString,
                   dataType: "html",
                   url: "../../../SetDateTimeline/"
               });
               setTimeout(function(){ location.reload(true); }, 100);
           });
       });
    });
})(jQuery);