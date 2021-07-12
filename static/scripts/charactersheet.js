window.onload = function() {
    var canvas = document.getElementById("sheetCanvas");
    var ctx = canvas.getContext("2d");
    var img = document.getElementById("sheet");
    ctx.drawImage(img, 350, 10);
};  