'use strict';

const handleLogin = document.querySelector('#login-button');

const loginForm = document.querySelector('#login')



loginForm.addEventListener('submit', (evt) => {

    evt.preventDefault();

    const formInputs = {
        email: document.querySelector('#email').value,
        pwd: document.querySelector('#pwd').value,
    };

    console.log(formInputs)

    fetch('/login', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then((response) => response.text())
        .then((respText) => {
            console.log(respText)
            if (respText == 'Success') {
                    handleLogin.innerText = 'Log Out';
                    document.location.href = "/fav_books";
                  }

            else {
                alert('Unable to Login! Please Try Again!');
            }


        });

});

