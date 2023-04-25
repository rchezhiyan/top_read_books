function Book(props) {
    console.log(props)
    console.log(props.book.id)
    return (
            <div className="card d-flex flex-column"  width="50">
                <img src={`https://covers.openlibrary.org/b/isbn/${props.book.isbn13}-M.jpg`} className="card-img-top" alt="..."/>
                <div className="card-body">
                    <h6 className="card-title">{props.book.title}</h6>
                </div>
                <div className="card-footer">
                    <a href={`/books/${props.book.id}`} class="btn btn-primary">See Details</a>
                </div>
            </div>

    )
    
}

const BookList = (props) => {
    const bookitems = [];

    console.log(props.books)
    
    for (const book in props.books) {
        console.log(props.books[book].title)
        bookitems.push(
            <Book book={props.books[book]}
            key={book}
            title={props.books[book].title}
            />
        );
    }

    return <div className="row row-cols-1 row-cols-md-2 g-4">{bookitems}</div>;

}

function Search() {

    const [searchtxt, setSearchtxt] = React.useState("");

    const [booklist, setBooklist] = React.useState([]);

    const handleSearch = (evt) => {
        evt.preventDefault();
        alert(`search text : ${searchtxt}`)

        fetch('/search.json', {
            method: 'POST',
            body: JSON.stringify({searchtxt}),
            headers: {
                'Content-Type': 'application/json',
            },
            })
            .then((response) => response.json())
            .then((responsejson) => {
                setBooklist((responsejson))

            });

    }


    return (
    <div>
        <form onSubmit={handleSearch}>
        <label>Search Text:
            <input
                type="text"
                value={searchtxt}
                onChange={(evt) => setSearchtxt(
                    evt.target.value
                )}
            />
        </label>
        <input type="submit" value="Search"/>
        </form>  
            
        <BookList books={booklist}/>


    </div>
   
  );
}

ReactDOM.render(<Search />, document.getElementById('search'));