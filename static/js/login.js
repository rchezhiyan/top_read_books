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
                    alert('You have Logged In!');
                  }

            else {
                alert('Unable to Login! Please Try Again!');
            }


        });

});

handleLogin.addEventListener('click',() => {

    fetch('/logout')
        .then((response) => response.text())
        .then((respText) => {
            if (respText == 'Success') {
                handleLogin.innerText = 'Log In';
                alert('You have Logged Out!');
            }

        });

});