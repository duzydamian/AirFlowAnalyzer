window.onload=function () {
  reimg1=document.getElementById('re1')
  reimg2=document.getElementById('re2')
  reimg3=document.getElementById('re3')
  reimg4=document.getElementById('re4')
  reimg5=document.getElementById('re5')
  reimg6=document.getElementById('re6')
  setInterval(function () {
    reimg1.src=reimg1.src.replace(/\?.*/,function () {
      return '?'+new Date()
    })
    reimg2.src=reimg2.src.replace(/\?.*/,function () {
      return '?'+new Date()
    })
    reimg3.src=reimg3.src.replace(/\?.*/,function () {
      return '?'+new Date()
    })
    reimg4.src=reimg4.src.replace(/\?.*/,function () {
      return '?'+new Date()
    })
    reimg5.src=reimg5.src.replace(/\?.*/,function () {
      return '?'+new Date()
    })
    reimg6.src=reimg6.src.replace(/\?.*/,function () {
      return '?'+new Date()
    })                
  },500)
  setInterval(function(){
  var includes = $('.include');
  jQuery.each(includes, function(){
    var file = $(this).data('include');
    $(this).load(file);
  });
},500)
}
