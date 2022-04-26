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
    $(".show-hide-btn").click(function() {
        $(this).parent().closest('div').children("p").toggleClass("d-none");
    })
  })
