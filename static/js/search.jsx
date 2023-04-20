function Search() {

    const [searchtxt, setSearchtxt] = React.useState("");

    const handleSearch = (evt) => {
        evt.preventDefault();
        alert(`search text : ${searchtxt}`)

        const searchData = {
            keyword: searchtxt,
        };

        fetch('/search.json', {
            method: 'POST',
            body: JSON.stringify(searchData),
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then((response) => response.json())
            .then((responsejson) => {
                console.log(responsejson)
            });

    }

  return (
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
        
  );
}

ReactDOM.render(<Search />, document.getElementById('search'));