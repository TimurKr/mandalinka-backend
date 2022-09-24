document.addEventListener("DOMContentLoaded", function () {

    const btnSubm = document.querySelector('#submit')

    const MyAccountForm = document.getElementById('MyAccount')
    
    MyAccountForm.addEventListener('submit',event => {
        if (!MyAccountForm.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            scroll(top);
        }
        MyAccountForm.classList.add('was-validated');
    }, false)
});
