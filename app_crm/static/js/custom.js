$(".notification-toggle").click(function (e) {
  e.stopPropagation();
  console.log("toggling sidebar");
    $(".notification-sidebar").toggleClass('active');

});
$(".cancel").click(function () {
  console.log("toggling visibility");
    $(this).parent().toggleClass('gone');

});

$('#content-wrapper').click(function() {
  if ($(".notification-sidebar").hasClass("active")) {
    $(".notification-sidebar").removeClass('active');
  }
})