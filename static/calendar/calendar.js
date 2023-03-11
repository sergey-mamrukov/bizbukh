const urlajax = `http://127.0.0.1:5000`;
let d = new Date() 
let y = d.getFullYear();
let m = d.getMonth();
/// берем сегодняшнюю дату

let place = document.getElementById("calendar");


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
                <tr class = "days"></tr>
                </thead>
                <tbody class = "info"></tbody>
            </table>
        </div>
    </div>
</div>`;


let modalhtml = `
<div class="modal modal-blur modal-lg fade show ttt" tabindex="-1" aria-labelledby="exampleModalLabel" style="display: block;" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel"></h5>
                <button type="button" onclick = closemodal() class="btn-close " data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">

            </div>

            <div class="modal-footer">
                <div class="input-group mb-3">
                    <input type="text" class="form-control input_name_pevent" placeholder="Название события">
                    <button class="btn btn-outline-info btn_add_pevent">Добавить событие</button>
                </div>
            </div>
        </div>
    </div>
</div>
<div class="modal-backdrop fade show"></div>`;

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

let alertnotdata = `
<div class="alert alert-danger alert1" role="alert">
  <h4 class="alert-title">Недостаточно данных&hellip;</h4>
  <div class="text-muted">Недостаточно данных для формирования графика. Исправьте данные о компаниях или создайте новые.</div>
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



function addalert(){
    cardbody = document.querySelector(".card-body1");
    alert1 = document.querySelector(".alert1");
    if (!alert1) {cardbody.innerHTML = alertnotdata;}
}

function delalert(){
    alert1 = document.querySelector(".alert1");
    if(alert1){alert1.remove()}
}

function cleartbody(){
    let tbody = document.querySelector(".info");
    tbody.innerHTML = "";//обнуляем таблицу для перерисовки данных
}//очистка тела таблицы с данными (дни не удаляются, только информация о клиентах и событиях)






function viewcal(){
    place.innerHTML = card;
    drawdays()
}

viewcal()



function drawdays(){

    let rowdays = document.querySelector(".days");
    rowdays.innerHTML = `<td class = "border" style = "min-width:170px; height:40px;" > </td>`;
                    
    
    let date = new Date(y,m+1,0);//

    let count_day = date.getDate();//считаем количество дней в месяце
  
    for(let i =0; i < count_day; i++){
      let t = getWeekDay(new Date(y,m,i).getDay())//заполняем строчку днями

      if(t == "Сб" || t=="Вс"){
      rowdays.innerHTML += `<td style = "min-width:40px; height:40px;" class = "text-center p-0 border text-danger"><div>${i+1}</div>${t}</td>`;  
      }//красим выходные красным цветом
      else{
          rowdays.innerHTML += `<td style = "min-width:40px; height:40px; "class = "text-center p-0 align-middle border"><div>${i+1}</div> ${t}</td>`;  
      }//обычные дни
      
      let dateinfo = document.querySelector(".caltitle");
      dateinfo.textContent =  `${getNameMonth(m)} - ${y} года`;//вывод информации в хлебных крошках
    }

     drawinfo();//вызов функции заполнения информацией
     changeButtonName();//вызов функции смены названия кнопок предыдущего и следующео месяца
     
      
  }//формирование календаря

  async function drawinfo(){
    addloader();
    url = `${urlajax}/ajax/get`
    
    let response = await fetch(url); 
    let info = await response.json(); // читаем ответ в формате JSON

    if(info.length == 0){ 
        cleartbody();
        addalert();
        return;
    }

    let date = new Date(y,m+1,0);
    let count_day = date.getDate();
    
    let tbody = document.querySelector(".info");

    // tbody.innerHTML = "";//обнуляем таблицу для перерисовки данных
    cleartbody();

    for(item in info){
        let client_info = document.createElement("tr");

        client_info.innerHTML += 
        `<td class = " border text-wrap p-0 ps-1" style = "width:170px; min-height:41px; position:absolute; background-color:#ffffff;">
        <div class = "" href = "http://127.0.0.1:5000/client/${info[item].client_id}">${info[item].clientname}</div>
        </td>`;

        //проходимся по дням
        for (let i = 1; i <= count_day; i++){

            let countevent = 0;//счетчик событий на определенный день
            let countready = 0;//счетчик выполненных событий
            let countproof = 0;//счетчие подтвержденных событий

            let curdate = dateFormater(new Date(y,m,i))//текущая дата (отформатированная)
            let events = info[item].events//список всех событий клиента на определенную дату


            //проходимся по событиям
            for(e in events){  
                if (info[item].events[e].dataend == curdate && info[item].events[e].status != "Не выполняется") {
                    countevent ++;
                    if (info[item].events[e].status == "Выполнено"){
                        countready ++;
                    }

                    if (info[item].events[e].status == "Подтверждено"){
                        countproof ++;
                    }
                }
            }


            
            //проверка количества событий со статусоми вывод с окрашиванием в разные цвета
            if(countevent >0){
                if(countevent == countproof){
                   client_info.innerHTML += `<td style = "width:40px; min-height:40px;" onclick = openmodal("${info[item].client_id}","${curdate}") class = "text-center border p-0  bg-success text-light pointer">OK</td>`;            
                }

                if(countevent == countready+countproof && countevent != countproof){
                    client_info.innerHTML += `<td style = "width:40px; min-height:40px;" onclick = openmodal("${info[item].client_id}","${curdate}") class = "text-center border p-0 bg-success-subtle text-secondary pointer"><div>${countevent}</div><div>${countready+countproof}</div></td>`;
                
                }

                if(countready+countproof < countevent){
                    client_info.innerHTML += `<td style = "width:40px; min-height:40px;" onclick = openmodal("${info[item].client_id}","${curdate}") class = "text-center border p-0  bg-danger-subtle text-secondary pointer"><div>${countevent}</div><div>${countready+countproof}</div></td>`;
                }
               

            }
            else{
               client_info.innerHTML += `<td style = "width:40px; min-height:40px;" onclick = 'openmodal("${info[item].client_id}","${curdate}")' class = "text-center border p-0 bg-light text-light pointer"><div>0</div><div>0</div></td>`;
            }
        }

        tbody.appendChild(client_info);
        
    }
    delloader();
    

}//вывод информации в таблицу


///////helper/////////
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
    cleartbody()
    changeButtonName()
    drawdays();
}//обработка нажатия на следующий месяц

function btnprev(){
    if(m!=0){
        m -= 1;
    }
    else {
        y -=1;
        m = 11;
    }
    cleartbody()
    changeButtonName()
    drawdays();
}//обработка нажатия на предыдущий месяц


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






  async function getclientinfo(clientid, date){

    let url = `${urlajax}/ajax/get?clientid=${clientid}&date=${date}`
    let response = await fetch(url); 
    let info = await response.json(); // читаем ответ в формате JSON


    let modaltitle = document.querySelector(".modal-title");
    modaltitle.textContent = `${date} - ${info.clientname}`

    let bodymodal = document.querySelector(".modal-body");
    bodymodal.innerHTML = "";//обнуляем тело модалки



    
    for(e in info.events){
        
        if(!info.events[e].ispersonal){
            //добавляем общее событие

            let card = document.createElement("div");
            card.classList.add("card","mt-2","shadow-none", "border-secondary");

            let cardheader = document.createElement("div");
            cardheader.classList.add("card-header");

            let cardactions = document.createElement("div");
            cardactions.classList.add("card-actions");

            let  btn_del = `
                    <button onclick = changestatus(${clientid},${info.events[e].eventid},4,"${date}") class="btn btn-ghost-secondary w-100">
                    Не выполняется
                    </button>
                `;

            cardactions.innerHTML = btn_del;    
            
            let eventtitle = document.createElement("h6");
            eventtitle.classList.add("card-title");
            eventtitle.textContent = `${info.events[e].nameevent} | ${info.events[e].status}`


            let cardbody = document.createElement("div");
            cardbody.classList.add("card-body");

            cardheader.appendChild (eventtitle);
            cardheader.appendChild(cardactions);
            
            card.appendChild(cardheader);

            let btn_ok = `<button class="btn btn-warning me-3" onclick = changestatus(${clientid},${info.events[e].eventid},1,"${date}")> Выполнено </button>`;
            let bnt_no = `<button class="btn btn-danger me-3" onclick = changestatus(${clientid},${info.events[e].eventid},2,"${date}")> Отменить выполнение </button>`;
            let bnt_proof = `<button class="btn btn-success me-3" onclick = changestatus(${clientid},${info.events[e].eventid},3,"${date}")> Подтвердить </button>`;
           
            
            cardbody.innerHTML += `Действие с событием</br>`

            if(info.events[e].status == "Не выполнено"){
                
                cardbody.innerHTML+=btn_ok;

            }

            if(info.events[e].status == "Выполнено"){
                cardbody.innerHTML+=bnt_proof;
                cardbody.innerHTML+=bnt_no;
 

            }

            if(info.events[e].status == "Подтверждено"){
                cardbody.innerHTML+=bnt_no;     
      
            }
        
            card.append(cardbody);
            bodymodal.append(card)
        }
        else if(info.events[e].ispersonal && info.events[e].clientid == clientid){        
      
            //добавляем персональное событие
            let card = document.createElement("div");
            card.classList.add("card","mt-2","shadow-none", "border-info");

            let cardheader = document.createElement("div");
            cardheader.classList.add("card-header");

            let cardactions = document.createElement("div");
            cardactions.classList.add("card-actions");

            let  btn_del = `
                    <button onclick = del_personal_event(${clientid},${info.events[e].eventid},3,"${date}") class="btn btn-ghost-danger w-100">
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-trash-x" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                        <path d="M4 7h16"></path>
                        <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12"></path>
                        <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3"></path>
                        <path d="M10 12l4 4m0 -4l-4 4"></path>
                    </svg>
                    Удалить событие
                    </button>
                `;

            cardactions.innerHTML = btn_del;    
            
            let eventtitle = document.createElement("h6");
            eventtitle.classList.add("card-title");
            eventtitle.textContent = `${info.events[e].nameevent} | ${info.events[e].status}`


            let cardbody = document.createElement("div");
            cardbody.classList.add("card-body");

            cardheader.appendChild (eventtitle);
            cardheader.appendChild(cardactions);
            
            card.appendChild(cardheader);

            let btn_ok = `<button class="btn btn-warning me-3" onclick = change_personal_status(${clientid},${info.events[e].eventid},1,"${date}")> Выполнено </button>`;
            let bnt_no = `<button class="btn btn-danger me-3" onclick = change_personal_status(${clientid},${info.events[e].eventid},2,"${date}")> Отменить выполнение </button>`;
            let bnt_proof = `<button class="btn btn-success me-3" onclick = change_personal_status(${clientid},${info.events[e].eventid},3,"${date}")> Подтвердить </button>`;
           
            
            cardbody.innerHTML += `Действие с событием</br>`

            if(info.events[e].status == "Не выполнено"){
                
                cardbody.innerHTML+=btn_ok;

            }

            if(info.events[e].status == "Выполнено"){
                cardbody.innerHTML+=bnt_proof;
                cardbody.innerHTML+=bnt_no;
 

            }

            if(info.events[e].status == "Подтверждено"){
                cardbody.innerHTML+=bnt_no;     
      
            }
        
            card.append(cardbody);
            bodymodal.append(card)
        }
    }  
 

}

async function changestatus(clientid, eventid, status, date){
    urlchange = `${urlajax}/ajax/changestatus/${clientid}/${eventid}/${status}`;
    
    let response = await fetch(urlchange); 
    let info = await response.json(); // читаем ответ в формате JSON
    
    // drawinfo()
    getclientinfo(clientid,date);
}

async function change_personal_status(clientid, eventid, status, date){
    urlchange = `${urlajax}/ajax/changestatuspersonal/${clientid}/${eventid}/${status}`;
    
    let response = await fetch(urlchange); 
    let info = await response.json(); // читаем ответ в формате JSON
    
    // drawinfo()
    getclientinfo(clientid,date);
}

async function del_personal_event(clientid, eventid, status, date){
    urlchange = `${urlajax}/ajax/delpersonalevent/${clientid}/${eventid}/${status}`;
    
    let response = await fetch(urlchange); 
    let info = await response.json(); // читаем ответ в формате JSON
    
    // drawinfo()
    getclientinfo(clientid,date);
}


function closemodal(){
    let modal = document.querySelector(".ttt");
    let modalbackdrop = document.querySelector(".modal-backdrop");

    cleartbody();

    modal.remove();
    modalbackdrop.remove();
    drawinfo();
}// функция закрытия модального окна

function openmodal(clientid, date){

    place.innerHTML += modalhtml;

    let bnt_add_pevent = document.querySelector(".btn_add_pevent");    

    bnt_add_pevent.setAttribute("onclick",`addpevent("${clientid}","${date}")`);



    getclientinfo(clientid, date)

}//функция открытия модального окна


async function addpevent(clientid, date){
    let input_name_pevent = document.querySelector(".input_name_pevent")
    pevent_name = input_name_pevent.value


        if (pevent_name != ""){

            console.log(pevent_name)
            pevent_info = {
                "eventname":pevent_name,
                "clientid":clientid,
                "date":date
            };

            console.log(`send date - ${date}`)
            console.log(`send client - ${clientid}`)

            console.log(pevent_info)

            await fetch("http://127.00.1:5000/ajax/addpevent/",{method:'POST', body:JSON.stringify(pevent_info)});
            
            input_name_pevent.value = "";
            //drawinfo();
            getclientinfo(clientid,date);
        }
}