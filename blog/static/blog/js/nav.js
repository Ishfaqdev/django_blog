$(document).ready(function(){
  $('.nav-link').click(function(){
    console.log('Clicked!');
    $('.nav-link').removeClass('active');
    $(this).addClass('active');
  });
});

