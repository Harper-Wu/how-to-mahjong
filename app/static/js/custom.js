
jQuery("#backtotop").click(function () {
    jQuery("body,html").animate({
        scrollTop: 0
    }, 600);
});
jQuery(window).scroll(function () {
    if (jQuery(window).scrollTop() > 150) {
        jQuery("#backtotop").addClass("visible");
    } else {
        jQuery("#backtotop").removeClass("visible");
    }
});

  var today = new Date();
  var expiry = new Date(today.getTime() + 30 * 24 * 3600 * 1000); // plus 30 days

function setCookie(name, value){
    document.cookie=name + "=" + escape(value) + "; path=/; expires=" + expiry.toGMTString();
}
function save(){
  $('.auto-save').savy('load');
}
function dstry(){
  //$('.auto-save').savy('destroy') --> can be used without callback
  $('.auto-save').savy('destroy');
}
function clear(){
  $.window.localStorage.clear();
}
