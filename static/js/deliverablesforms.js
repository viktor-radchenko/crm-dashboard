$(".fformselect").on("click", function(){
    $(this).data('val', $(this).val());
});

$(".fformselect").on("change", function() {
    if ($(this).val() === ""){
        $("#" + $(this).data('val')).hide();
    } else {
        $("#" + $(this).val()).show().siblings().hide();
    }
})

$(document).ready(function() {
    let areas = document.querySelectorAll("textarea");
    let heightLimit = 200; /* Maximum height: 200px */

    areas.forEach(a => {
        a.oninput = function() {
            a.style.height = ""; /* Reset the height*/
            a.style.height = Math.min(a.scrollHeight, heightLimit) + "px";
        }
    });
    $(".show-hide-btn").click(function() {
        $(this).parent().closest('div').children("p").toggleClass("d-none");
    });
  });
