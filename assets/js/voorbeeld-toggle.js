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
    if (!(event.target.classList.contains("toggle_header") || event.target.classList.contains("toggle_header_open"))) return;
    var parentElement = event.target.parentElement;
    var parentElementChildren = parentElement.children;
    for (var i = 0; i < parentElementChildren.length; i ++) {
        var childElement = parentElementChildren[i];
        if (!(childElement.classList.contains("toggle_header") || childElement.classList.contains("toggle_header_open"))) {
            toggle(childElement);
        }
    }
    if (event.target.classList.contains("toggle_header")) {
        event.target.classList.remove("toggle_header");
        event.target.classList.add("toggle_header_open");
    } else {
        event.target.classList.remove("toggle_header_open");
        event.target.classList.add("toggle_header");
    }
}, false);
