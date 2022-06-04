$(document).ready( function() {
  $(document).on('change', '.btn-file :file', function() {
    console.log($(this))
    var input = $(this);
    var label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [label]);
  });

  function readProfileURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      
      reader.onload = function (e) {
        $('#img-upload1').attr('src', e.target.result);
      }
      reader.readAsDataURL(input.files[0]);
    }
  }

  function readAgencyURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      
      reader.onload = function (e) {
        $('#img-upload2').attr('src', e.target.result);
        $('#img-upload2').removeAttr("style");
      }
      reader.readAsDataURL(input.files[0]);
    }
  }

  $("#imgInp1").change(function(){
      readProfileURL(this);
  });
  
  $("#imgInp2").change(function(){
    readAgencyURL(this);
}); 
});