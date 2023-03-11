const urlajax = `http://127.0.0.1:5000`;
let d = new Date()
let y = d.getFullYear();
let m = d.getMonth();
let clientid = document.querySelector(".clientid").textContent;
let place = document.querySelector(".place");


let loader = `
<div class = "card loader1">
    <div class = "card-body">
        <div class="text-center container-slim mt-3 ">
            <div class="mb-2">
                <span class=" bg-primary text-white avatar">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-hourglass-empty" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                <path d="M6 20v-2a6 6 0 1 1 12 0v2a1 1 0 0 1 -1 1h-10a1 1 0 0 1 -1 -1z"></path>
                <path d="M6 4v2a6 6 0 1 0 12 0v-2a1 1 0 0 0 -1 -1h-10a1 1 0 0 0 -1 1z"></path>
                </svg>
                </span>

            </div>
            <div class="text-muted mb-3">Подождите, данные загружаются</div>
            <div class="progress progress-sm">
                <div class="progress-bar progress-bar-indeterminate"></div>
            </div>
        </div>
    </div>
</div>`;

function addloader(){
    loader1 = document.querySelector(".loader1");
    if (!loader1) {place.innerHTML += loader;}
}//добавление лоадера

function delloader(){
    loader1 = document.querySelector(".loader1");
    if(loader1){loader1.remove();}
    
}//удаление лоадера


async function getinfo() {

    place.innerHTML = "";
    addloader()
    let responce = await fetch(`${urlajax}/ajax/get?clientid=${clientid}`)
    let info = await responce.json()

    console.log(info)

    


    for (let month = 0; month <= 11; month++) {

        let table = document.createElement("table");
        table.classList.add("table", "table-vcenter", "card-table")
        let header = document.createElement("thead");
        let headerrow = document.createElement("tr");
        headerrow.innerHTML = `
                        <th class = "col-5">Название события</th>
                        <th class = "col-1">Дата</th>
                        <th class = "col-2">Статус</th>
                        <th class = "col">Действие</th>
                        `;

        let card = document.createElement("div");
        card.classList.add("card", "mb-3");

        let date = new Date(y, month + 1, 0);
        let count_day = date.getDate();//считаем количество дней в месяце

        let cardheader = `
        <div class = "card-header">
            <h5 class = "card-title">События за ${getNameMonth(month)}</h5>
        </div>
        `;

        let cardbody = document.createElement("div");
        cardbody.classList.add("card-body");

        card.innerHTML += cardheader;
        card.appendChild(cardbody);



        let tbody = document.createElement("tbody");
        table.appendChild(tbody);
        header.appendChild(headerrow);
        table.appendChild(header);




        for (let day = 1; day <= count_day; day++) {


            for (item in info['events']) {

                let col = document.createElement("tr");

                col.innerHTML += `<td >${info['events'][item]['nameevent']}</td>`;
                col.innerHTML += `<td >${info['events'][item]['dataend']}</td>`;

                if (info['events'][item].status == "Не выполнено") {
                    col.innerHTML += `<td class = "text-danger">Не выполнено</td>`
                }
                if (info['events'][item].status == "Выполнено") {
                    col.innerHTML += `<td class = "text-warning">Выполнено (не подтверждено)</td>`
                }
                if (info['events'][item].status == "Подтверждено") {
                    col.innerHTML += `<td class = "text-success">Выполнено (подтверждено)</td>`
                }
                if (info['events'][item].status == "Не выполняется") {
                    col.innerHTML += `<td class = "text-secondary">Не выполняется</td>`
                }

                let btn_ok = '';
                let btn_no = '';
                let btn_proof = '';
                let btn_not = '';

              

                if (!info['events'][item].ispersonal) {

                    btn_ok = `<button class="btn btn-outline-success" onclick = changestatus(${info['client_id']},${info['events'][item].eventid},1)> Выполнить </button>`;
                    btn_no = `<button class="btn btn-outline-danger" onclick = changestatus(${info['client_id']},${info['events'][item].eventid},2)> Отменить </button>`;
                    btn_proof = `<button class="btn btn-success" onclick = changestatus(${info['client_id']},${info['events'][item].eventid},3)> Подтвердить </button>`;
                    btn_not = `<button class="btn btn-outline" onclick = changestatus(${info['client_id']},${info['events'][item].eventid},4)> Не выполнется </button>`;
                    btn_not_no = `<button class="btn btn-outline" onclick = changestatus(${info['client_id']},${info['events'][item].eventid},5)> Выполняется </button>`;
                }
                else{
                    btn_ok = `<button class="btn btn-outline-success" onclick = change_personal_status(${info['client_id']},${info['events'][item].eventid},1)> Выполнить </button>`;
                    btn_no = `<button class="btn btn-outline-danger" onclick = change_personal_status(${info['client_id']},${info['events'][item].eventid},2)> Отменить </button>`;
                    btn_proof = `<button class="btn btn-success" onclick = change_personal_status(${info['client_id']},${info['events'][item].eventid},3)> Подтвердить </button>`;
                    btn_not = `<button class="btn btn-outline" onclick = del_personal_event(${info['client_id']},${info['events'][item].eventid},4)> Удалить событие </button>`;

                }


                if (info['events'][item].status == "Не выполнено") {
                    col.innerHTML += `<td>
                <div class = "row">
                    <div class = "col-4">${btn_ok}</div>
                    <div class = "col-4">${btn_not}</div>
                    <div class = "col-4"></div>
                </div>
                </td>`
                }

                if (info['events'][item].status == "Не выполняется") {
                    col.innerHTML += `<td>
                <div class = "row">
                    <div class = "col-4">${btn_not_no}</div>
                    <div class = "col-4"></div>
                    <div class = "col-4"></div>
                </div>
                </td>`
                }

                if (info['events'][item].status == "Выполнено") {
                    col.innerHTML += `<td>
                <div class = "row">
                    <div class = "col-4">${btn_proof}</div>
                    <div class = "col-4">${btn_no}</div>
                    <div class = "col-4"></div>
                </div>
                </td>`
                }

                if (info['events'][item].status == "Подтверждено") {
                    col.innerHTML += `<td>
                <div class = "row">
                    <div class = "col-4"></div>
                    <div class = "col-4">${btn_no}</div>
                    <div class = "col-4"></div>
                </div>
                </td>`
                }


                if (info['events'][item].dataend == dateFormater(new Date(y, month, day))) {
                    tbody.appendChild(col)
                }

                // if (info['events'].length == 0) {
                //     cardbody.innerHTML = `
                //     <div class="alert border-0 bg-light-warning alert-dismissible fade show py-2">
                //         <div class="d-flex align-items-center">
                //             <div class="fs-3 text-warning"><i class="bi bi-exclamation-triangle-fill"></i></div>

                //             <div class="ms-3">
                //                 <div class="text-warning">Нет событий для выполнения</div>
                //             </div>
                //         </div>
                //     </div>`;
                // }
                // else { cardbody.appendChild(table) }


                cardbody.appendChild(table)
                place.appendChild(card)


            }


        }


    }
    delloader()
}
getinfo()

async function changestatus(clientid, eventid, status) {
    urlchange = `http://127.0.0.1:5000/ajax/changestatus/${clientid}/${eventid}/${status}`;

    // let response = 
    await fetch(urlchange);
    table = document.querySelector("table")
    table.remove()

    getinfo();
}

async function change_personal_status(clientid, eventid, status) {
    urlchange = `${urlajax}/ajax/changestatuspersonal/${clientid}/${eventid}/${status}`;

    let response = await fetch(urlchange);
    let info = await response.json(); // читаем ответ в формате JSON

    getinfo();
}

async function del_personal_event(clientid, eventid, status){
    urlchange = `${urlajax}/ajax/delpersonalevent/${clientid}/${eventid}/${status}`;
    
    let response = await fetch(urlchange); 
    let info = await response.json(); // читаем ответ в формате JSON
    
    getinfo();
}








function splitdate(date) {
    let d = date.split("-")
    result = [Number(d[0]), Number(d[1])]
    return result;
}

// splitdate()

function getNameMonth(monthNumber) {
    switch (monthNumber) {
        case 0: return "Январь"
        case 1: return "Февраль"
        case 2: return "Март"
        case 3: return "Апрель"
        case 4: return "Май"
        case 5: return "Июнь"
        case 6: return "Июль"
        case 7: return "Август"
        case 8: return "Сентябрь"
        case 9: return "Октябрь"
        case 10: return "Ноябрь"
        case 11: return "Декабрь"

    }
}//возвращает название месяцев


function dateFormater(date) {
    var day = date.getDate();
    var month = date.getMonth() + 1;
    var year = date.getFullYear();

    if (day < 10) {
        day = '0' + day;
    }
    if (month < 10) {
        month = '0' + month;
    }

    return year + '-' + month + '-' + day;
}//возвращает дату в нужном формате