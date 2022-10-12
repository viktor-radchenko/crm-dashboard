let $profileBtn = $('.header__profile');
let $notificationBtn = $('.header__notifications-toggle');
let $sidebarBtn = $('.header__burger-btn');
let $sidebarLink = $('.sidebar__link--expandable');

$(function () {
  $('body').on('click', function (e) {
    $('.show').removeClass('show');
  });
});

$profileBtn.on('click', function (e) {
  e.stopPropagation();
  $('.notifications', $profileBtn).toggleClass('show');
});

$notificationBtn.on('click', function (e) {
  e.stopPropagation();
  let popupContainer = $('.notifications', $(this).parent());
  popupContainer.toggleClass('show');

  $(this).on('blur', function () {
    console.log('ORU NAFIG');
    popupContainer.removeClass('show');
  });
});

// initialise sidebar
$(function () {
  let collapsed = localStorage.getItem('isCollapsed') === 'true';
  console.log(collapsed);
  if (collapsed) {
    $('.sidebar').addClass('collapsed');
  } else {
    $('.sidebar').toggleClass('collapsed');
    localStorage.setItem('isCollapsed', $('.sidebar').hasClass('collapsed'));
  }
});

$sidebarBtn.on('click', function (e) {
  e.stopPropagation();
  $('.sidebar').toggleClass('collapsed');
  localStorage.setItem('isCollapsed', $('.sidebar').hasClass('collapsed'));
});

$sidebarLink.on('click', function (e) {
  e.stopPropagation();
  $(this).toggleClass('show');
  let $popup = $('.sidebar__popup', $(this));
  $popup.toggleClass('show');

  $(this).focusout(function () {
    $popup.removeClass('show');
  });
});

// All orders DataTable initialise
$(function () {
  if ($('#dataTable').length) {
    $('#dataTable').DataTable({
      lengthMenu: [50, 10, 25],
    });

    $('#dataTable_filter').appendTo($('.all-orders__search-container'));

    // Hide plugin search button
    $('#dataTable_filter > label').contents()[0].remove();

    // Append icon to the search and style it
    let $tableFilter = $('input[type=search]', $('#dataTable_filter'));
    $tableFilter.attr('placeholder', 'Search by Order #, Client etc.');

    // Some fine touches to pagination settings
    $('select[name=dataTable_length]').css({
      margin: '0 5px',
      padding: '5px',
      background: 'none',
      outline: 'none',
      borderRadius: '5px',
    });

    // Add event listeners to link expanders
    $('.all-orders__link-expander').each(function (idx) {
      $(this).on('click', function () {
        $(this).next().toggleClass('all-orders__link-popup--hidden');
      });
    });
  }
});

// CRUD DataTable initialise
$(function () {
  if ($('#dataTableCrud').length) {
    $('#dataTableCrud').DataTable({
      lengthMenu: [50, 10, 20],
    });

    $('#dataTableCrud_filter').appendTo($('.crm-crud__search'));

    // Hide plugin search button
    $('#dataTableCrud_filter > label').contents()[0].remove();

    // Add margins
    $('#dataTableCrud_length').css({marginBottom: '40px'})
    $('select[name=dataTableCrud_length]').css({
      margin: '0 5px',
      padding: '5px',
      background: 'none',
      outline: 'none',
      borderRadius: '5px',
    });

    // Append icon to the search and style it
    let $tableFilter = $('input[type=search]', $('#dataTableCrud_filter'));
    $tableFilter.attr('placeholder', 'Search');
  }
});

// All orders magic
$(function () {
  if ($('.custom-select').length) {
    console.log('Wtfc');
    $('.custom-select').each(function () {
      var classes = $(this).attr('class'),
        id = $(this).attr('id'),
        name = $(this).attr('name');
      var template = '<div class="' + classes + '">';
      template += '<span class="custom-select-trigger">' + $(this).attr('placeholder') + '</span>';
      template += '<div class="custom-options">';
      $(this)
        .find('option')
        .each(function () {
          template +=
            '<span class="custom-option ' +
            $(this).attr('class') +
            '" data-value="' +
            $(this).attr('value') +
            '">' +
            $(this).html() +
            '</span>';
        });
      template += '</div></div>';

      $(this).wrap('<div class="custom-select-wrapper"></div>');
      $(this).hide();
      $(this).after(template);
    });
    $('.custom-option:first-of-type').hover(
      function () {
        $(this).parents('.custom-options').addClass('option-hover');
      },
      function () {
        $(this).parents('.custom-options').removeClass('option-hover');
      }
    );
    $('.custom-select-trigger').on('click', function () {
      $('html').one('click', function () {
        $('.custom-select').removeClass('opened');
      });
      $(this).parents('.custom-select').toggleClass('opened');
      event.stopPropagation();
    });
    $('.custom-option').on('click', function () {
      $(this).parents('.custom-select-wrapper').find('select').val($(this).data('value'));
      $(this).parents('.custom-options').find('.custom-option').removeClass('selection');
      $(this).addClass('selection');
      $(this).parents('.custom-select').removeClass('opened');
      $(this).parents('.custom-select').find('.custom-select-trigger').text($(this).text());
    });
  }
});

/*Dropdown Menu*/
$(function () {
  if ($('.dropdown').length) {
    $('.dropdown').on('click', function () {
      $(this).attr('tabindex', 1).focus();
      $(this).toggleClass('active');
      $(this).find('.dropdown-menu').slideToggle(150);

      $(this).focusout(function () {
        $(this).removeClass('active');
        $(this).find('.dropdown-menu').slideUp(150);
      });
      $('.dropdown .dropdown-menu li').click(function () {
        $(this).parents('.dropdown').find('span').text($(this).text());
        $(this).parents('.dropdown').find('input').attr('value', $(this).attr('data-value'));
      });
    });
  }
});
/*End Dropdown Menu*/

// Flash messages 
$(function () {
  let flash_msgs = $('.flash-msg__close')
  if (flash_msgs.length) {
    flash_msgs.on('click', function() {
      $(this).parent().toggleClass('close');
      // $(this).parent().slideUp(300);
    })
  }
})