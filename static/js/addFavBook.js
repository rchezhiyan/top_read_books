'use strict';


const addbutton = document.querySelector('.Add_Fav_Book')
const removebutton = document.querySelector('.Rem_Fav_Book')
const bkid = location.pathname.split('/').pop()

const url_add = `/add_book?book_id=` + bkid;

const url_remove = `/remove_book?book_id=` + bkid;

if (addbutton) {

    addbutton.addEventListener('click', () => {
        fetch(url_add)
            .then((response) => response.text())
            .then((respText) => {
                console.log(respText)
                if (respText == 'Success') {
                    alert('Added book to your list!');
                }else {
                    alert(respText);
                }
            });
    });

}

if (removebutton){
    removebutton.addEventListener('click', () => {
        fetch(url_remove)
            .then((response) => response.text())
            .then((respText) => {
                console.log(respText)
                if (respText == 'Success') {
                    alert('Removed the book from your list!');
                }else {
                    alert(respText);
                }
            });
    });
}
