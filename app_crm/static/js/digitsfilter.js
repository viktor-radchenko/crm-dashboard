function setInputFilter(textbox, inputFilter) {
    ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
      textbox.addEventListener(event, function() {
        if (inputFilter(this.value)) {
          this.oldValue = this.value;
          this.oldSelectionStart = this.selectionStart;
          this.oldSelectionEnd = this.selectionEnd;
        } else if (this.hasOwnProperty("oldValue")) {
          this.value = this.oldValue;
          this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
        } else {
          this.value = "";
        }
      });
    });
  }

order_inputs = document.querySelectorAll('[name="order"]');
order_inputs.forEach(o => setInputFilter(o, function(value) {
  return /^\d*$/.test(value); }))

// setInputFilter(document.getElementById("order"), function(value) {
// return /^\d*$/.test(value); });

month_inputs = document.querySelectorAll('[name="month"]');
month_inputs.forEach(o => setInputFilter(o, function(value) {
  return /^\d*$/.test(value); }))
  