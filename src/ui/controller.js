"use strict"

var cmodel = new model(),
    cview = new view(),
    ccontroller = null;

function controller() {
    this.updateDisplay = function () {
        cmodel.init();
        cview.setOtherEventFunc();
        cview.setOtherTagFunc();
        cview.generateSongListForm();
        cview.setUserAgreement();
    };

    this.initial = function () {
        ccontroller.updateDisplay();
    };

}

ccontroller = new controller();
window.addEventListener("load", ccontroller.initial);
console.log('started controller');