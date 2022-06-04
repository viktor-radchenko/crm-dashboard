$(".notification-toggle").click(function (e) {
  e.stopPropagation();
    $(".notification-sidebar").toggleClass('active');
});

$(".cancel").click(function () {
  $(this).parent().toggleClass('gone');
  let id = $(this).parent().attr('data-id');
  $.ajax({url: `/notifications/delete/${id}`});
});

$('#content-wrapper').click(function() {
  if ($(".notification-sidebar").hasClass("active")) {
    $(".notification-sidebar").removeClass('active');
  }
})

function processNotifications() {
  let notifications = $('.notification.notification-bold');
  console.log(notifications);
  if (notifications.length > 0) {
    $('.notification-count').removeClass("gone");
  }
};

processNotifications();

// $("#accordionSidebar").hover(function() {
//   setTimeout(function() {
//     $("#accordionSidebar").toggleClass("toggled")
//   }, 2000);
// })