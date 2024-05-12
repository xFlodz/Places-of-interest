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

document.addEventListener("DOMContentLoaded", function() {
    var toolbarOptions = [
        ['bold', 'italic', 'underline', 'link'],
        [{ 'align': [] }],
        [{ 'color': [] }, { 'background': [] }],
        ['clean']
    ];

    var quill = new Quill('#editor', {
        theme: 'snow',
        modules: {
            toolbar: toolbarOptions
        }
    });

    quill.root.innerHTML = document.querySelector('#text').value;

    quill.on('text-change', function() {
        var editorContent = quill.root.innerHTML;
        document.querySelector('#text').value = editorContent;
    });
});

