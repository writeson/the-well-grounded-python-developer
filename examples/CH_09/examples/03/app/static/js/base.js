(function() {
    var option = {
        animation: true,
        delay: 3000
    }
    var toastElements = [].slice.call(document.querySelectorAll('.toast'))
    toastElements.map(function (toastElement) {
        toast = new bootstrap.Toast(toastElement, option)
        toast.show()
    })
}())
