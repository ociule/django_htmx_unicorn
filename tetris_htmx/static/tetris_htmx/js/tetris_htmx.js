document.addEventListener('keydown', function(event) {
    if(event.keyCode == 37) {
        console.log('Left was pressed');
        document.getElementsByName("left")[0].click()
    }
    else if(event.keyCode == 38) {
        console.log('Up was pressed');
        document.getElementsByName("up")[0].click()
    }
    else if(event.keyCode == 39) {
        console.log('Right was pressed');
        document.getElementsByName("right")[0].click()
    }
    else if(event.keyCode == 40) {
        console.log('Down was pressed');
        document.getElementsByName("down")[0].click()
    }
});
