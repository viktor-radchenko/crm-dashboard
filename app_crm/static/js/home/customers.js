$(document).ready(function() {
    $('.customer-wrapper').slick({
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        speed: 300,
        dots: true
    });
});

// my slick slider as const object
const mySlider = $('.customer-wrapper').on('init', function(slick) {

    // set this slider as const for use in set time out
    const slider = this;
      
    // slight delay so init completes render
    setTimeout(function() {
  
      // dot buttons
      let dots = $('.slick-dots > LI > BUTTON', slider);
  
      // each dot button function
      $.each(dots, function(i,e) {
  
        // slide id
        let slide_id = $(this).attr('aria-controls');
        
        // custom dot image
        let dot_img = $('#'+slide_id).data('dot-img');
        
        $(this).html('<img src="' + dot_img + '" alt="" />');
  
      });
  
    }, 100);
  
  
})