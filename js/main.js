const HeaderEl = document.getElementById("header")

window.addEventListener("scroll", function () {
    const scrollPos = window.scrollY
    if(scrollPos > 10){
        HeaderEl.classList.add("header-mini")
    }
    else{
        HeaderEl.classList.remove("header-mini")
    }
})