window.onload=function () {
  setInterval(function(){
  var includes = $('.include');
  jQuery.each(includes, function(){
    var file = $(this).data('include');
    $(this).load(file);
  });
},500)
}