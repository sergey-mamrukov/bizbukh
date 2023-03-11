async function getinfo(){
    let eventid = document.querySelector(".eventid").textContent
    let url = `http://127.0.0.1:5000/ajax/getallclientsforevent/${eventid}`

    let cardbody = document.querySelector(".card-body")
    

    let response = await fetch(url); 
    let info = await response.json(); // читаем ответ в формате JSON

    let table = document.createElement("table")

    table.classList.add("table","table-vcenter", "card-table")

    let header = document.createElement("thead");
    let headerrow = document.createElement("tr");
    headerrow.innerHTML = `<th class = "col-6">Название компании</th>
                        <th class = "col">Статус выполнения</th>
                        <th class = "col">Действие</th>
                        `;
    header.appendChild(headerrow);
    table.appendChild(header);

    let tbody = document.createElement("tbody");
    table.appendChild(tbody);

    for (item in info){
        let col = document.createElement("tr");

        col.innerHTML += `<td >${info[item].clientname}</td>`;
        if( info[item].status == null){
            col.innerHTML += `<td class = "text-danger">Не выполнено</td>`
        }
        if( info[item].status == "Не выполнено"){
            col.innerHTML += `<td class = "text-danger">Не выполнено</td>`
        }
        if( info[item].status == "Выполнено"){
            col.innerHTML += `<td class = "text-warning">Выполнено (не подтверждено)</td>`
        }
        if( info[item].status == "Подтверждено"){
            col.innerHTML += `<td class = "text-success">Выполнено (подтверждено)</td>`
        }
        if( info[item].status == "Не выполняется"){
            col.innerHTML += `<td class = "text-secondary">Не выполняется</td>`
        }
            
        let btn_ok = `<button class="btn btn-outline-success" onclick = changestatus(${info[item].clientid},${eventid},1)> Выполнить </button>`;
        let bnt_no = `<button class="btn btn-outline-danger" onclick = changestatus(${info[item].clientid},${eventid},2)> Отменить </button>`;
        let bnt_proof = `<button class="btn btn-success" onclick = changestatus(${info[item].clientid},${eventid},3)> Подтвердить </button>`;
        
        if(info[item].status == "Не выполнено"){
            col.innerHTML += `<td>
            <div class = "row">
                <div class = "col-6">${btn_ok}</div>
                <div class = "col-6"></div>
            </div>
            </td>`
        }
        if(info[item].status == "Выполнено"){
            col.innerHTML += `<td>
            <div class = "row">
                <div class = "col-6">${bnt_proof}</div>
                <div class = "col-6">${bnt_no}</div>
            </div>
            </td>`
        }

        if(info[item].status == "Подтверждено"){
            col.innerHTML += `<td>
            <div class = "row">
                <div class = "col-6"></div>
                <div class = "col-6">${bnt_no}</div>
            </div>
            </td>`
        }
        if(info[item].status == "Не выполняется"){
            col.innerHTML += `<td></td>`
        }

        tbody.appendChild(col)
    }


    if (info.length == 0){
        cardbody.innerHTML = `<div class="alert border-0 bg-light-warning alert-dismissible fade show py-2">
        <div class="d-flex align-items-center">
          <div class="fs-3 text-warning"><i class="bi bi-exclamation-triangle-fill"></i>
          </div>
          <div class="ms-3">
            <div class="text-warning">Событие не требует выполнения</div>
          </div>
        </div>
      </div>`
    }
    else{cardbody.appendChild(table)}
}


async function changestatus(clientid, eventid, status){
    urlchange = `http://127.0.0.1:5000/ajax/changestatus/${clientid}/${eventid}/${status}`;
    
    // let response = 
    await fetch(urlchange); 
    table = document.querySelector("table")
    table.remove()

    getinfo();
}

getinfo();