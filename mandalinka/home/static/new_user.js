document.addEventListener("DOMContentLoaded", function () {
    // Code for tab < > buttons
    // Mapping to next tab
    document.querySelector('#btn-next').onclick = function () {
        document.querySelector('.nav .active').parentElement.nextElementSibling.querySelector('button').click()
    };
    // Mapping to prev tabs
    document.querySelector('#btn-prev').onclick = function () {
        document.querySelector('.nav .active').parentElement.previousElementSibling.querySelector('button').click()
    };

    const tabs = document.querySelectorAll('.nav li');
    const btnNext = document.querySelector('#btn-next');
    const btnPrev = document.querySelector('#btn-prev');
    const btnSubm = document.querySelector('#submit')

    // Disable and enable < > buttons for first and last
    tabs.forEach(function (tab) {
        let button = tab.querySelector('button');
        if (tab === tabs[0]) {
            button.onclick = function () {
                btnPrev.setAttribute('disabled', '');
                btnNext.removeAttribute('disabled');
                btnSubm.setAttribute('disabled', '');
                scroll(top);
            }
        } else if (tab === tabs[tabs.length - 1]) {
            button.onclick = function () {
                btnNext.setAttribute('disabled', '');
                btnPrev.removeAttribute('disabled');
                btnSubm.removeAttribute('disabled');
                scroll(top);
            }
        } else {
            button.onclick = function () {
                btnNext.removeAttribute('disabled');
                btnPrev.removeAttribute('disabled');
                btnSubm.setAttribute('disabled', '');
                scroll(top);
            }
        }
    });
    const SignupForm = document.getElementById('SignupForm')
    
    SignupForm.addEventListener('submit',event => {
        if (!SignupForm.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            document.querySelector('.nav').firstElementChild.firstElementChild.click();
            scroll(top);
        }
        SignupForm.classList.add('was-validated');
    }, false)
});
