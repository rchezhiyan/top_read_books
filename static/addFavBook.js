'use strict';


const addbutton = document.querySelector('.Add-Fav_Book')
const bkid = location.pathname.split('/').pop()

const url = `/add_book?book_id=` + bkid;


addbutton.addEventListener('click', () => {
    fetch(url)
        .then((response) => response.text())
        .then((respText) => {
            console.log(respText)
            if (respText == 'Success') {
                alert('Added book to your list!');
            }else {
                alert('Failed to add.');
            }
        });
});