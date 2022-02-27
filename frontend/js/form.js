async function postForm(url, data)
{
    config =
    {
        method: "POST",
        credentials: "same-origin", //TODO change?
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data) //TODO JSON.stringify?
    }

    await fetch (url, config)
    .then(response => response.json())
    .then(data =>
        {
            if (url.includes("covid"))
            {
                toptable = document.createElement("table")

                const tr = toptable.insertRow()
                const td = tr.insertCell()
                td.innerHTML = "<b>Country</b>"
                td.style.border = '1px solid black';
                const td2 = tr.insertCell()
                td2.innerHTML = "<b>Number</b>"
                td2.style.border = '1px solid black';

                
                for (row of data.top)
                {
                    console.log(row)
                    const tr = toptable.insertRow()
                    for (const [key, val] of Object.entries(row))
                    {
                        console.log(val)
                        const td = tr.insertCell()
                        td.textContent = val
                        td.style.border = '1px solid black';
                        
                    }
                }
                result.innerHTML = ""
                result.appendChild(toptable)

                bottomtable = document.createElement("table")

                const tr2 = bottomtable.insertRow()
                const td3 = tr2.insertCell()
                td3.innerHTML = "<b>Country</b>"
                td3.style.border = '1px solid black';
                const td4 = tr2.insertCell()
                td4.innerHTML = "<b>Number</b>"
                td4.style.border = '1px solid black';

                
                for (row of data.bottom)
                {
                    console.log(row)
                    const tr = bottomtable.insertRow()
                    for (const [key, val] of Object.entries(row))
                    {
                        console.log(val)
                        const td = tr.insertCell()
                        td.textContent = val
                        td.style.border = '1px solid black';
                        
                    }
                }


                result.appendChild(bottomtable)
                // console.log(data.top)

                // bottomtable = document.createElement("table")
                // for (row of data.bottom)
                // {
                //     console.log(row.countryname)
                // }
            }
            else if (data.hasOwnProperty('error'))
            {
                // console.log(data.error)
                result.textContent = "There has been an error in your query. Check that the connection is active and that the query is valid.";
            }
            else if (Object.keys(data).length === 0)
            {
                // console.log("Success")
                result.innerHTML = "If you were trying to Insert a User / Visit, you were successful. <br> If you were trying to Select from the database, your query had an error."
            }
            else if (Array.isArray(data.data))
            {
                if (typeof data.data[0] === 'string' || data.data[0] instanceof String)
                {
                    table = document.createElement("table")

                    const tr = table.insertRow()
                    const td = tr.insertCell()
                    td.innerHTML = "<b>Country</b>"
                    td.style.border = '1px solid black';

                    for (val of data.data)
                    {
                        const tr = table.insertRow()
                        const td = tr.insertCell()
                        td.textContent = val
                        td.style.border = '1px solid black';
                    }

                    result.innerHTML = ""
                    result.appendChild(table)
                }
                else
                {
                    console.log(data.data)

                    table = document.createElement("table")

                    const tr = table.insertRow()

                    for (const [key, value] of Object.entries(data.data[0]))
                    {
                        const td = tr.insertCell()
                        td.innerHTML = `<b>${key}</b>`
                        td.style.border = '1px solid black';
                    }
                    
                    for (val of data.data)
                    {
                        console.log(val)
                        const tr = table.insertRow()
                        for (const [key, value] of Object.entries(val))
                        {
                            console.log( value)
                            const td = tr.insertCell()
                            td.textContent = value
                            td.style.border = '1px solid black';
                        }
                    }

                    result.innerHTML = ""
                    result.appendChild(table)


                }
            }
            else
            {
                let text = "";
                
                for (const [key, value] of Object.entries(data.data))
                {
                    
                    if (typeof value === 'string' || value instanceof String
                        || typeof value === 'number' || value instanceof Number)
                    {
                        console.log(value)
                        text = text + `${key}  :  ${value}\n`
                    }
                    else //value is an array
                    {
                        console.log(value)
                        if (value !== null)
                        {
                            for (const obj of value)
                            {
                                console.log(obj)
                                for (const [nk, nv] of Object.entries(obj))
                                    text = text + `${nk}  :  ${nv}\n`
                            }
                        }
                    }
                }
                console.log(text)
                result.innerText=text
            }
        }
    )
}

function submitForm(event)
{
    event.preventDefault();

    const data = new FormData(event.target)
    const formJSON = Object.fromEntries(data.entries());

    postForm(endpoint, formJSON)

}

const form = document.getElementById('form');
const endpoint = form.dataset.url
const result = document.getElementById('result');
form.addEventListener('submit', submitForm);
