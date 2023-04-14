'use strict';

const handleLogin = document.querySelector('#logout-button');

handleLogin.addEventListener('click',(evt) => {
    
    evt.preventDefault()
    
    fetch('/logout')
        .then((response) => response.text())
        .then((respText) => {
            if (respText == 'Success') {
                handleLogin.innerText = 'Log In';
                alert('You have Logged Out!');
            }

        });

});