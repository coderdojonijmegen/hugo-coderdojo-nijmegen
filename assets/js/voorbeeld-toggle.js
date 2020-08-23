var show = function(elem) {
    elem.style.display = "block";
}

var hide = function(elem) {
    elem.style.display = "none";
}

var toggle = function(elem) {
    if (window.getComputedStyle(elem).display == "block") {
        hide(elem);
    } else {
        show(elem);
    }
}

document.addEventListener('click', function(event) {
    if (!event.target.classList.contains("toggle_header")) return;
    var parentElement = event.target.parentElement;
    var parentElementChildren = parentElement.children;
    for (var i = 0; i < parentElementChildren.length; i ++) {
        var childElement = parentElementChildren[i];
        if (!childElement.classList.contains("toggle_header")) {
            toggle(childElement);
        }
    }
}, false);
