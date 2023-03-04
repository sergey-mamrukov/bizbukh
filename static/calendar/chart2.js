const urlajax = `http://127.0.0.1:5000`;
let d = new Date()
let y = d.getFullYear();
// let m = d.getMonth();
let m =1;
/// берем сегодняшнюю дату

let allevents = []

let place = document.getElementById("chart");


let card = `
<div class="card">
    <div class="card-header">
        <h3 class="card-title caltitle"></h3>
        <div class="card-actions">
            <button onclick = 'btnprev()'class="btn prev"></button>
            <button onclick = 'btnnext()'class="btn next"></button>
        </div>
    </div>
    <div class="card-body card-body1">
        <div class="table-responsive">
            <table class = 'table'>
                <thead>
                <tr class = "eventrow"></tr>
                </thead>
                <tbody class = "info"></tbody>
            </table>
        </div>
    </div>
</div>`;



let loader = `
<div class="text-center container-slim mt-3 loader1">
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
</div>`;


function addloader(){
    cardbody = document.querySelector(".card-body1");
    loader1 = document.querySelector(".loader1");
    if (!loader1) {cardbody.innerHTML += loader;}
}//добавление лоадера

function delloader(){
    loader1 = document.querySelector(".loader1");
    if(loader1){loader1.remove();}
    
}//удаление лоадера

function cleartbody(){
    let tbody = document.querySelector(".info");
    tbody.innerHTML = "";//обнуляем таблицу для перерисовки данных
}//очистка тела таблицы с данными (дни не удаляются, только информация о клиентах и событиях)


function clearevent(){
    let eventrow = document.querySelector(".eventrow");
    eventrow.innerHTML = "";//обнуляем таблицу для перерисовки данных
}//очистка строки с событиями



place.innerHTML = card

let cardbody = document.querySelector(".card-body1");

async function drawevents() {
    // url = `${urlajax}/ajax/getallevents`
    // cardbody.appendChild(spinner);
    addloader();

    let dateinfo = document.querySelector(".caltitle");
      dateinfo.textContent =  `${getNameMonth(m)} - ${y} года`;//вывод информации в хлебных крошках

    let eventrow = document.querySelector(".eventrow")


    let response = await fetch(`${urlajax}/ajax/getallevents`);
    let info = await response.json(); // читаем ответ в формате JSON

    eventrow.innerHTML = `<td style = "min-width:170px;" class = " "> </td>`;//вывод названия месяца в первой ячейке таблицы
// <h4>${getNameMonth(m)}</h4>


    let date = new Date(y, m + 1, 0);//
    let count_day = date.getDate();//считаем количество дней в месяце

    // console.log(date)

    for (let i = 1; i <= count_day; i++) {
        let curdate = dateFormater(new Date(y, m, i))//текущая дата (отформатированная)

        for (item in info) {

            if (info[item].dataend == curdate) {

                eventrow.innerHTML += `
                <td  style = "min-width:150px; height:80px;" class = "border p-1 text-center align-middle">
                    <div class = "row text-center  top-50">
                        <a  class = "text-wrap" href = "${urlajax}/calendar/change/${info[item].eventid}"> ${info[item].shortname}</a>
                    </div>

                    <div class = "row text-center top-50">
                        <span>(${info[item].type_event})</span>
                    </div>

                    <div class = "row text-center top-50">
                        <div class = "text-secondary">${info[item].dataend}</div>
                    </div>
                           
                </td>`;

                allevents.push(info[item])
            }
        }
    }


    // let dateinfo = document.querySelector(".dateinfo");
    // dateinfo.textContent = `на ${getNameMonth(m)} - ${y} года`;//вывод информации в хлебных крошках
    delloader();
    drawinfo();
    changeButtonName()//вызов функции смены названия кнопок предыдущего и следующео месяца 


}


async function drawinfo(){
    url = `http://127.0.0.1:5000/ajax/get`

    addloader()

    let response = await fetch(url); 
    let info = await response.json(); // читаем ответ в формате JSON

    let tbody = document.querySelector(".info");


    tbody.innerHTML = "";//обнуляем таблицу для перерисовки данных


    for(item in info){
        let client_info = document.createElement("tr");

        client_info.innerHTML += 
        `<td class = " border text-wrap p-0 ps-1" style = "width:170px; min-height:41px; position:absolute; background-color:#ffffff;">
        <div class = "" href = "http://127.0.0.1:5000/client/${info[item].client_id}">${info[item].clientname}</div>
        </td>`;

        let clientevents = info[item].events
        let actual = []

        for (e in allevents){
            for(el in clientevents){
                if(clientevents[el].eventid == allevents[e].eventid){
                    actual.push(clientevents[el])
                }
            }
           
        }

        console.log(allevents)

        for(e in allevents){
            let nullcol = true;

          

            for(a in actual){ 
                if(allevents[e].eventid == actual[a].eventid){
                    if(actual[a].status == "Подтверждено"){
                        client_info.innerHTML += `<td style = "width:170px; height:41px;" class = "border text-center align-middle p-0 bg-success text-light">Подтверждено</td>`;
                    }
                    if(actual[a].status == "Выполнено"){
                        client_info.innerHTML += `<td style = "width:170px; height:41px;" class = "border text-center align-middle p-0 bg-success-subtle text-secondary">Выполнено</td>`;
                    }
                    if(actual[a].status == "Не выполнено"){
                        client_info.innerHTML += `<td style = "width:170px; height:41px;" class = "border text-center align-middle p-0 bg-danger-subtle text-secondary">Не выполнено</td>`;
                    }

                    if(actual[a].status == "Не выполняется"){
                        client_info.innerHTML += `<td style = "width:170px; height:41px;" class = "border text-center align-middle p-0 bg-dark-subtle text-secondary">Не выполняется</td>`;
                    }

                    if(actual[a].status == "None"){
                        client_info.innerHTML += `<td style = "width:170px; height:41px;" class = "border text-center align-middle p-0 bg-danger-subtle text-secondary">Не выполнено</td>`;
                        // ${actual[a].status}
                    }
                    
                    nullcol= false
                }            
            }


            if(nullcol){
                client_info.innerHTML += `<td class = "border  bg-light text-secondary"> </td>`;
            }
        }

        tbody.appendChild(client_info);
    }
    delloader();
}//вывод информации в таблицу




changeButtonName()
drawevents()















/////////// вспомогательные функции

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


  function changeButtonName(){
    let btnprev = document.querySelector(".prev")
    let btnnext = document.querySelector(".next")

    if (m == 0){btnprev.textContent = getNameMonth(m+11);}
    else{btnprev.textContent = getNameMonth(m-1);}

    if(m == 11){btnnext.textContent = getNameMonth(m-11);}
    else{btnnext.textContent = getNameMonth(m+1)}
}//меняет название месяцев на кнопках

function btnnext(){
    if(m!=11){
        m += 1;
    }
    else {
        y +=1;
        m = 0;
    }
    allevents = [];
    clearevent();
    cleartbody();
    drawevents();
}//обработка нажатия на следующий месяц

function btnprev(){
    if(m!=0){
        m -= 1;
    }
    else {
        y -=1;
        m = 11;
    }
    allevents = [];
    clearevent();
    cleartbody();
    drawevents();
}//обработка нажатия на предыдущий месяц


function getWeekDay(dayNumber){
    switch(dayNumber+1)
    {
        case 7: return "Вс";
        case 1: return "Пн";
        case 2: return "Вт";
        case 3: return "Ср";
        case 4: return "Чт";
        case 5: return "Пт";
        case 6: return "Сб";
    } 
}//возвращает название дней недели

function getNameMonth(monthNumber){
    switch(monthNumber){
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