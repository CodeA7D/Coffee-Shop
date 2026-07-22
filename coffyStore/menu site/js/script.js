let open = document.querySelector("#menu-open");
let close = document.querySelector("#menu-close");

let menu = document.querySelector(".navbar");

let head = document.querySelector("header");

open.addEventListener("click", function () {
    menu.classList.toggle("active");

    if (menu.classList.contains("active")) {
        menu.style.left = "0";
        head.style.cssText = "content:''; position: fixed; left: 0; top: 0; height: 100%; width: 100%; backdrop-filter: blur(5px); background-color: rgba(0, 0, 0, 0.2);";
    }

});

close.addEventListener("click", function () {
    menu.classList.toggle("active");

    if (menu.classList.contains("active")) {
        menu.style.left = "-300px";
        head.style.cssText = "";
    }
});