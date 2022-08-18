$window = $(window);
$window.scroll(function() {
  $scroll_position = $window.scrollTop();
    if ($scroll_position > 100) { // if body is scrolled down by 300 pixels
        $('.header-wrapper').addClass('sticky');

        // to get rid of jerk
        header_height = $('.header-wrapper').innerHeight();
        $('body').css('padding-top' , header_height);
    } else {
        $('body').css('padding-top' , '0');
        $('.header-wrapper').removeClass('sticky');
    }
 });


$('.column-box_wrapper').click(function() {
    $(this).toggleClass('active-box');
});


$(document).ready(function() {
    $('.recipes-slider').slick({
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 1,
        speed: 300,
        dots: false
    });
});


$('.work-boxes_wrapper').on('click', '.column-box_wrapper', function(){
    var src = $(this).attr('data-src');
    $('.boxes-image').attr('src', src);
});