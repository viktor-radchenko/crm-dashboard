$(document).ready(function() {
    var wrapper = $(".spe-container");
    var add_button = $(".add_text_field");
    var add_checkbox_button = $(".add_checkbox_field");
    var add_radio_button = $(".add_radio_field");
    var add_textarea_button = $(".add_textarea");
    var add_dropdown_button = $(".add_dropdown");

    $(add_button).click(function(e) {
        e.preventDefault();
        $(wrapper).append('<div class="form-group col-12 m-2 p-2 card mb-4 shadow tosendgroup"><label class="text ml-1">Title:</label><input type="text" class="form-control mb-2" name="textfield" required><a href="#" class="delete">Delete</a></div>');
    });

    $(add_checkbox_button).click(function(e) {
        e.preventDefault();
        $(wrapper).append('<div class="form-group col-12 m-2 p-2 mb-4 card shadow tosendgroup"><label class="text ml-1">Checkbox field. Title:</label><input type="text" class="form-control mb-2" name="checkboxname" required><div class="checkboxes"><label class="text ml-1">Checkbox:</label><br><a href="#" class="addcheckbox">Add checkbox</a></div><a href="#" class="delete">Delete group</a></div>');
    });

    $(add_dropdown_button).click(function(e) {
        e.preventDefault();
        $(wrapper).append('<div class="form-group col-12 m-2 p-2 card mb-4 shadow tosendgroup"><label class="text ml-1">Dropdown field. Title:</label><input type="text" class="form-control mb-2" name="dropdownname" required><div class="dropdown_items"><label class="text ml-1">Dropdow item:</label><br><a href="#" class="adddropdownitem">Add dropdown item</a></div><a href="#" class="delete">Delete group</a></div>');
    });

    $(add_radio_button).click(function(e) {
        e.preventDefault();
        $(wrapper).append('<div class="form-group col-12 m-2 p-2 mb-4 card shadow tosendgroup"><label class="text ml-1">Radio field. Title:</label><input type="text" class="form-control mb-2" name="radioname" required><div class="radios"><label class="text ml-1">Radio:</label><br><a href="#" class="addradio">Add radio</a></div><a href="#" class="delete">Delete group</a></div>');
    });

    $(add_textarea_button).click(function(e) {
        e.preventDefault();
        $(wrapper).append('<div class="form-group col-12 m-2 p-2 card mb-4 shadow tosendgroup"><label class="text ml-1">Text area title:</label><input type="text" class="form-control mb-2" name="textarea" required><a href="#" class="delete">Delete</a></div>');
    });

    $(wrapper).on("click", ".delete", function(e) {
        e.preventDefault();
        $(this).parent('div').remove();
    });

    $(wrapper).on("click", ".addcheckbox", function(e) {
        e.preventDefault();
        $(this).parent('div').append('<div class="checkbox m-2 p-2 card"><input type="text" class="form-control mb-2 col-10" name="checkboxitem" required><a href="#" class="delete">Delete checkbox</a></div>');
    });

    $(wrapper).on("click", ".addradio", function(e) {
        e.preventDefault();
        $(this).parent('div').append('<div class="radio m-2 p-2 card"><input type="text" class="form-control mb-2 col-10" name="radioitem" required><a href="#" class="delete">Delete radio</a></div>');
    });

    $(wrapper).on("click", ".adddropdownitem", function(e) {
        e.preventDefault();
        $(this).parent('div').append('<div class="dropdown_item m-2 p-2 card"><input type="text" class="form-control mb-2 col-10" name="dropdownitem" required><a href="#" class="delete">Delete dropdown item</a></div>');
    });
});

function setVals() {
    var blockcounting = 0
    $('.tosendgroup').each(function(index) {
        var allinputs = this.getElementsByTagName('input');
        $(allinputs).each(function(){
            var tempval = this.name.replace(/[0-9]/g, '');
            this.name = tempval + index;
            console.log(this.name);
        });
        blockcounting++;
    });
    var totcou = document.getElementById('totalcount');
    totcou.value = blockcounting;
};