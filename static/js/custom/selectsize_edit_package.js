const dragArea = document.querySelector(".draggable")
new Sortable(dragArea, {
    animation: 350
});

function reOrder() {
    let curindex = 0;
    $('.inputcheck').each(function() {


        if (this.checked){
            if (this.value.split(":").length === 1) {
                let firstval = this.value.split(":")[0];
                this.value = curindex + ":" + firstval;
                curindex++;
            } else if (this.value.split(":").length === 2) {
                let secondval = this.value.split(":")[1];
                this.value = curindex + ":" + secondval;
                curindex++;
            }
            
        };
    });
};