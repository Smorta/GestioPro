(function ($) {
    $(function() { // cette ligne est équivalente à $(document).ready(function(){})
       $(".task__detail").each(function () {
           $(this).parent().mouseleave(function () {//quand la souris passe sur l'element
               $(this).children(".task__detail").hide(); // permet de cacher des éléments a l'aide de sélecteur (les mêmes quand css)
           });
           $(this).parent().mouseenter(function () {//quand la souris ressort de l'element
               $(this).children(".task__detail").show();
           });
       });

       $('.task').draggable({
           cursor: 'move',
           containment: 'document',
       });

       $('.item').droppable({
           drop : handleTaskDrop,
           hoverClass: 'hovered',
       });

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

       function handleTaskDrop( event, ui ) {

           const draggable = ui.draggable;
           ui.draggable.position({of: $(this), my: 'left top', at: 'left top'});
           const ID = draggable.attr('id');
           const DGA = draggable.css("grid-area");
           const DataDrop = $(this).children().attr('value');
           const DataDrag = draggable.children().first().attr('value')
           console.log(DataDrag)
           const GC = $(this).css("grid-column");
           const jsonString = 'DataDrop=' + DataDrop + '&DataDrag=' + DataDrag + "&GC=" + GC + "&ID=" + ID + "&DGA=" + DGA;

           $.ajax({
               type: "POST",
               data: jsonString,
               dataType : "html",
               url: "../RefreshTimelineArchi/"
           });
           setTimeout(function(){ location.reload(true); }, 100);

       }

       $(".form-taskContainer").each(function () {
           $(this).children(".exit").click(function () {//quand la souris passe sur l'element
               $(this).parent().hide(400);// permet de cacher des éléments a l'aide de sélecteur (les mêmes quand css)
           });
       });
       $(".task").each(function () {
           $(this).click(function () {//quand la souris passe sur l'element
               $(this).children(".form-taskContainer").show(); // permet de cacher des éléments a l'aide de sélecteur (les mêmes quand css)
           });
       });
       $(".btn-secondary").each(function () {
           $(this).click(function () {//quand la souris passe sur l'element
               $(this).parent().parent().parent().hide(400); // permet de cacher des éléments a l'aide de sélecteur (les mêmes quand css)
           });
       });
       $("form").each(function () {
           $(this).submit(function(e){
               e.preventDefault();
               const phase_id = $(this).children("data").attr('value');
               const form_url = "../Phase/Save" + phase_id + "/";
               var form_method = $(this).attr("method");
               var form_data = $(this).serialize();
               console.log(form_data);
               $.ajax({
                   url : form_url,
                   type : form_method,
                   data : form_data
               });

               setTimeout(function(){ location.reload(true); }, 100);
           });
       });

       var itemWidth = $(".item").width() + 5;

       $(".task").resizable({
          handles: "e, w",
          grid: [ itemWidth , 10 ],
          stop: resizeStop,
       });

       function resizeStop(event, ui){
           var deltaWidth = Math.round((ui.size.width - ui.originalSize.width)/itemWidth);
           var deltaLeft = Math.round((ui.position.left - ui.originalPosition.left)/itemWidth);
           var ID = ui.element.attr('id');
           const jsonString = 'deltaWidth=' + deltaWidth + '&deltaLeft=' + deltaLeft + "&ID=" + ID;
            $.ajax({
               type: "POST",
               data: jsonString,
               dataType : "html",
               url: "../ResizeTask/"
           });
           setTimeout(function(){ location.reload(true); }, 100);
       }

       $(".Time-Selector a").each(function (){
           $(this).click(function () {
               var data = $(this).children("data").attr('value');
               const jsonString = 'data=' + data;
               $.ajax({
                   type: "POST",
                   data: jsonString,
                   dataType: "html",
                   url: "../SetDateTimeline/"
               });
               setTimeout(function(){ location.reload(true); }, 100);
           });
       });

    });

})(jQuery);