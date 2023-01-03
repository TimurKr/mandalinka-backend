document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })

    try {
        document.querySelector(".invalid-feedback").scrollIntoView({behavior: "smooth", block: "center", inline: "center"})
    } catch (e) {}
})