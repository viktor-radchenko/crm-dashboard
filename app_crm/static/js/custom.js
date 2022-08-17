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


var modal = document.getElementById("myModal");
var btn = document.getElementById("feedback__btn");
var span = document.getElementsByClassName("feedback__close")[0];

btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

$(function () {
  $('[data-toggle="tooltip"]').tooltip({placement:"auto"})
})