async function getinfo(){
    let eventid = document.querySelector(".eventid").textContent
    let url = `http://127.0.0.1:5000/ajax/getallclientsforevent/${eventid}`

    let cardbody = document.querySelector(".card-body")
    

    let response = await fetch(url); 
    let info = await response.json(); // читаем ответ в формате JSON

    let table = document.createElement("table")

    table.classList.add("table", "mt-3", "table-sm")

    let header = document.createElement("thead");
    let headerrow = document.createElement("tr");
    headerrow.innerHTML = `<th>Название компании</th>
                        <th>Статус выполнения</th>
                        <th>Действие</th>
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
            
        let btn_ok = `<button class="btn btn-outline-success px-5 me-3" onclick = changestatus(${info[item].clientid},${eventid},1)> Выполнить </button>`;
        let bnt_no = `<button class="btn btn-outline-danger px-5 me-3" onclick = changestatus(${info[item].clientid},${eventid},2)> Отменить выполнение </button>`;
        let bnt_proof = `<button class="btn btn-outline-success px-5 me-3" onclick = changestatus(${info[item].clientid},${eventid},3)> Подтвердить выполнение </button>`;
        
        if(info[item].status == "Не выполнено" || info[item].status == null){
            col.innerHTML += `<td>${btn_ok}</td>`
        }
        if(info[item].status == "Выполнено"){
            col.innerHTML += `<td>${bnt_proof} ${bnt_no} </td>`
        }

        if(info[item].status == "Подтверждено"){
            col.innerHTML += `<td>${bnt_no} </td>`
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
    
    let response = await fetch(urlchange); 
    // let info = await response.json(); // читаем ответ в формате JSON
    
    table = document.querySelector("table")
    table.remove()

    getinfo();
}

getinfo();