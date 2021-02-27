$(document).ready(function() {
  function stick() {
    if (window.pageYOffset >= $("#before-nav").height()) {
      navbar.addClass("sticky");
    } else {
      navbar.removeClass("sticky");
    }
  }
  
  var rellax = new Rellax(".rellax");
  
  var navbar = $("#navbar");
  var sticky = navbar.offset().top;
  
  $(".background").css("margin-top", "-" + $("#before-nav").height() + "px");
  
  $(window).scroll(stick);
  
  stick();
});