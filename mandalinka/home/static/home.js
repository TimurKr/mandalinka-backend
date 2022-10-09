// Code for Login

document.addEventListener("DOMContentLoaded", () => {
    const LoginModal = document.getElementById('LoginModal');
    if (LoginModal) {
        if (document.getElementById('LoginModal').classList.contains('active')){
            document.getElementById('LoginModalButton').click()
        }

        (() => {
            'use strict'
        
            const LoginForm = document.getElementById('LoginForm')
        
            LoginForm.addEventListener('submit', event => {
                if (!LoginForm.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                LoginForm.classList.add('was-validated');
            }, false)
        
        })()
    }

})


