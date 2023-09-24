var diffidx = 0;

$(document).ready(function() {
   // highlight all TOC items that point to pages with diffs
   $("li.toctree-l1 a").each(function() {
       $.ajax({
           url:$(this).attr("href"),
           type:'GET',
           success: function(data){
               //$('#content').html(.html());
               if ($(data).find('.bd-main ins:visible, .bd-main del:visible').length > 0){
               	   $(this).addClass('diff-highlighted')
               }
           }
       });
   })
   console.log($("li.toctree-l1 a").attr("href"));
   

   // highlight and scroll to the first diff element
   var cur;
   cur = $(".bd-main ins:visible,.bd-main del:visible").eq(diffidx)
   cur.addClass("diff-selected");
   $(cur)[0].scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest"});
});

$(document).on("keypress", function(e) {
   var cur;	
   var next;
   cur = $(".bd-main ins:visible,.bd-main del:visible").eq(diffidx)
   cur.removeClass("diff-selected");
   if (e.which == 110){
     diffidx += 1;
     if (diffidx > $(".bd-main ins:visible,.bd-main del:visible").length-1){
         diffidx = $(".bd-main ins:visible,.bd-main del:visible").length-1;
     }
   } 
   if (e.which == 78) {
     diffidx -= 1;
     if (diffidx < 0){
     	diffidx = 0;
     }
   }
   next = $(".bd-main ins:visible,.bd-main del:visible").eq(diffidx)
   next.addClass("diff-selected")
   $(next)[0].scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest"});
});
