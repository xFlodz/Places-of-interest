const HeaderEl = document.getElementById("header")

window.addEventListener("scroll", function () {
    const scrollPos = this.window.scrollY

    if(scrollPos > 80){
        HeaderEl.classList.add("header-mini")
    }
    else{
        HeaderEl.classList.remove("header-mini")
    }
    
})