/**
 * This self-invoking function displays all the Flask flash
 * messages that are queued up.
 */
(function() {
    const option = {
        animation: true,
        delay: 3000
    }
    var toastElements = [].slice.call(document.querySelectorAll('.toast'))
    toastElements.map((toastElement) => {
        toast = new bootstrap.Toast(toastElement, option)
        toast.show()
    })
}())
