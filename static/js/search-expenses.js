const searchFiled = document.getElementById('search-field');
const tableOutput = document.getElementById('table-output')
const appTable = document.getElementById('app-table')
const paginationContainer = document.getElementById('pagination-container')
const tbody = document.getElementById('table-output-tbody')

tableOutput.style.display = "none";

searchFiled.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;
    // console.log(searchText)

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = "none";
        tbody.innerHTML = ''

        fetch("search-expense", {
            body: JSON.stringify({'searchText': searchValue}),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log('Data', data);
                appTable.style.display = "none";
                tableOutput.style.display = "block";

                if (data.length === 0) {
                    tableOutput.innerHTML = "No results found."
                } else {
                    data.forEach(item => {
                        tbody.innerHTML += `<tr>
                        <td>${item.amount}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                    </tr>`
                    })
                }
            });
    } else {
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
        tableOutput.style.display = "none";
    }
});
