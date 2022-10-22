// Code for Login

document.addEventListener("DOMContentLoaded", () => {
    const LoginModal = document.getElementById('LoginModal')
    // Autofocus email field in modal
    if (LoginModal != null){
        LoginModal.addEventListener('shown.bs.modal', () => {
            document.getElementById('id_username').focus()
        })
        // Show on load if active
        if (LoginModal.classList.contains('active')){
            new bootstrap.Modal('#LoginModal').show()
        }
    }

    // Client side login verification
    const LoginForm = document.getElementById('LoginForm')
    if (LoginForm != null) {{
        'use strict'
        LoginForm.addEventListener('submit', event => {
            if (!LoginForm.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            LoginForm.classList.add('was-validated');
        }, false)
    }}
    
    
})


