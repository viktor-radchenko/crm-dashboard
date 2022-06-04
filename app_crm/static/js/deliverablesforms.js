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
    let areas = document.querySelectorAll(".textarea-expandable");
    let minHeight = 60; /* Maximum height: 200px */

    areas.forEach(a => {
        a.oninput = function() {
            if (a.scrollHeight > minHeight) a.style.height = a.scrollHeight + "px";
            if (a.value.length === 0) {
                a.scrollHeight = 60;
                a.style.height = 62 + "px";
            }
        }
    });
    $(".show-hide-btn").click(function() {
        $(this).parent().closest('div').children("p").toggleClass("d-none");
    });
  });
