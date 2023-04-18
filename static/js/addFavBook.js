'use strict';

const favbutton = document.querySelector('#fav_book')

const bkid = location.pathname.split('/').pop()

const url_add = `/add_book?book_id=` + bkid;
const url_remove = `/remove_book?book_id=` + bkid;



favbutton.addEventListener('click', (evt) => {
    evt.preventDefault();
    if (favbutton.innerText === "Add book to MyList") {
        fetch(url_add)
        .then((response) => response.text())
        .then((respText) => {
            console.log(respText)
            if (respText == 'Success') {
                alert('Added book to your list!');
                favbutton.innerText = "Remove book from MyList";
            }else {
                alert(respText);
            }
        });
    }
    else{
        fetch(url_remove)
            .then((response) => response.text())
            .then((respText) => {
                console.log(respText)
                if (respText == 'Success') {
                    alert('Removed the book from your list!');
                    favbutton.innerText = "Add book to MyList";
                }else {
                    alert(respText);
                }
            });
        }

    });





// if (favbutton.innerText === "Remove book from MyList"){

//     // const favbutton = document.querySelector('#fav_book button')

//     favbutton.addEventListener('click', (evt) => {
//         evt.preventDefault();
//         fetch(url_remove)
//             .then((response) => response.text())
//             .then((respText) => {
//                 console.log(respText)
//                 if (respText == 'Success') {
//                     alert('Removed the book from your list!');
//                     favbutton.innerText = "Add book to MyList";
//                 }else {
//                     alert(respText);
//                 }
//             });
//     });
// }
