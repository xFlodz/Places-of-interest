<<<<<<< HEAD
const HeaderEl = document.getElementById("header")

window.addEventListener("scroll", function () {
    const scrollPos = this.window.scrollY

    if(scrollPos > 80){
        HeaderEl.classList.add("header-mini")
    }
    else{
        HeaderEl.classList.remove("header-mini")
    }
    
=======
const HeaderEl = document.getElementById("header")

window.addEventListener("scroll", function () {
    const scrollPos = this.window.scrollY

    if(scrollPos > 80){
        HeaderEl.classList.add("header-mini")
    }
    else{
        HeaderEl.classList.remove("header-mini")
    }
    
>>>>>>> a0ed675aed43f254ef1706b2c98c02846467b2b3
})