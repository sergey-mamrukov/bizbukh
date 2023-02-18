let d = new Date() 
let y = d.getFullYear();
let m = d.getMonth();

let spinner = document.createElement('div');
    spinner.classList.add('spinner-border','position-absolute','top-50','start-50');
    spinner.setAttribute("role","status");

let cardbody = document.querySelector(".table");


function drawdays(){
    let rowdays = document.querySelector(".days");

    cardbody.appendChild(spinner);
    rowdays.innerHTML = `<td class = "border col-2 text-center align-middle">
                              <h4>${getNameMonth(m)}</h4>
                         </td>`;//вывод названия месяца в первой ячейке таблицы

    let date = new Date(y,m+1,0);//

    let count_day = date.getDate();//считаем количество дней в месяце
  
    for(let i =0; i < count_day; i++){
      let t = getWeekDay(new Date(y,m,i).getDay())//заполняем строчку днями
//   class="col-1"
      if(t == "Сб" || t=="Вс"){
      rowdays.innerHTML += `<td class = "text-center border col-1 text-danger"><div>${i+1}</div>${t}</td>`;  
      }//красим выходные красным цветом
      else{
          rowdays.innerHTML += `<td class = "text-center align-middle border col-1"><div>${i+1}</div> ${t}</td>`;  
      }//обычные дни
      
      let dateinfo = document.querySelector(".dateinfo");
      dateinfo.textContent =  `на ${getNameMonth(m)} - ${y} года`;}//вывод информации в хлебных крошках
    spinner.remove();
     drawinfo();//вызов функции заполнения информацией
     changeButtonName()//вызов функции смены названия кнопок предыдущего и следующео месяца
      
  }//формирование календаря


async function drawinfo(){
    url = `http://127.0.0.1:5000/ajax/get`
    cardbody.appendChild(spinner);
    let response = await fetch(url); 
    let info = await response.json(); // читаем ответ в формате JSON


    let date = new Date(y,m+1,0);
    let count_day = date.getDate();
    let tbody = document.querySelector(".info");

    tbody.innerHTML = "";//обнуляем таблицу для перерисовки данных


    for(item in info){
        let client_info = document.createElement("tr");
        client_info.classList.add("d-flex")

        client_info.innerHTML += 
        `<td class = "border col-2 text-light bg-secondary p-3">
        <a class = "text-light" href = "http://127.0.0.1:5000/client/${info[item].client_id}">${info[item].clientname}</a>
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
                if (info[item].events[e].dataend == curdate) {
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
                   client_info.innerHTML += `<td onclick = openmodal("${info[item].client_id}","${curdate}") class = "text-center border col-1 bg-success text-light pointer">OK</td>`;            
                }

                if(countevent == countready+countproof && countevent != countproof){
                    client_info.innerHTML += `<td onclick = openmodal("${info[item].client_id}","${curdate}") class = "text-center border col-1 bg-success-subtle text-secondary pointer">${countevent}-${countready+countproof}</td>`;
                
                }

                if(countready+countproof < countevent){
                    client_info.innerHTML += `<td onclick = openmodal("${info[item].client_id}","${curdate}") class = "text-center border col-1 bg-danger-subtle text-secondary pointer">${countevent}-${countready+countproof}</td>`;
                }
               

            }
            else{
               client_info.innerHTML += `<td onclick = 'openmodal("${info[item].client_id}","${curdate}")' class = "text-center border col-1 bg-light text-secondary pointer"></td>`;
            }
        }

        spinner.remove();
        tbody.appendChild(client_info);
    }
    

}//вывод информации в таблицу

async function getclientinfo(clientid, date){

    let url = `http://127.0.0.1:5000/ajax/get?clientid=${clientid}&date=${date}`
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
            card.classList.add("card", "mt-2");
            card.classList.add("shadow-none");
            card.classList.add("border");
            let cardbody = document.createElement("div");
            cardbody.classList.add("card-body");


            
            let eventtitle = document.createElement("h6");
            eventtitle.classList.add("card-title");
            eventtitle.textContent = `${info.events[e].nameevent} | ${info.events[e].status}`

            let btn_ok = `<button class="btn btn-warning me-3" onclick = changestatus(${clientid},${info.events[e].eventid},1,"${date}")> Выполнено </button>`;
            let bnt_no = `<button class="btn btn-danger me-3" onclick = changestatus(${clientid},${info.events[e].eventid},2,"${date}")> Отменить выполнение </button>`;
            let bnt_proof = `<button class="btn btn-success me-3" onclick = changestatus(${clientid},${info.events[e].eventid},3,"${date}")> Подтвердить </button>`;
            let bnt_notready = `<button class="btn btn-dark me-3" onclick = changestatus(${clientid},${info.events[e].eventid},4,"${date}")> Не выполняется </button>`;

            cardbody.append(eventtitle);
            cardbody.innerHTML += `Действие с событием</br>`



            if(info.events[e].status == "Не выполнено" || info.events[e].status == "None"){
                cardbody.innerHTML+=btn_ok;
                cardbody.innerHTML+=bnt_notready;
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
            card.classList.add("card","mt-2");
            card.classList.add("shadow-none");
            card.classList.add("border", "border-info");

            let cardbody = document.createElement("div");
            cardbody.classList.add("card-body");


            
            let eventtitle = document.createElement("h6");
            eventtitle.classList.add("card-title");
            eventtitle.textContent = `${info.events[e].nameevent} | ${info.events[e].status} | Персональное событие`

            let btn_ok = `<button class="btn btn-warning me-3" onclick = change_personal_status(${clientid},${info.events[e].eventid},1,"${date}")> Выполнено </button>`;
            let bnt_no = `<button class="btn btn-danger me-3" onclick = change_personal_status(${clientid},${info.events[e].eventid},2,"${date}")> Отменить выполнение </button>`;
            let bnt_proof = `<button class="btn btn-success me-3" onclick = change_personal_status(${clientid},${info.events[e].eventid},3,"${date}")> Подтвердить </button>`;
            let btn_del = `<button class="btn btn-secondary me-3" onclick = del_personal_event(${clientid},${info.events[e].eventid},3,"${date}")> Удалить событие </button>`;
            cardbody.append(eventtitle);
            cardbody.innerHTML += `Действие с событием</br>`



            if(info.events[e].status == "Не выполнено" || info.events[e].status == "None"){
                cardbody.innerHTML+=btn_ok;
                cardbody.innerHTML+=btn_del;

            }

            if(info.events[e].status == "Выполнено"){
                cardbody.innerHTML+=bnt_proof;
                cardbody.innerHTML+=bnt_no;
                cardbody.innerHTML+=btn_del;
            }

            if(info.events[e].status == "Подтверждено"){
                cardbody.innerHTML+=bnt_no;
                cardbody.innerHTML+=btn_del;
            }

            card.append(cardbody);
            bodymodal.append(card)

        }
    } 

    

    

    
}

async function changestatus(clientid, eventid, status, date){
    urlchange = `http://127.0.0.1:5000/ajax/changestatus/${clientid}/${eventid}/${status}`;
    
    let response = await fetch(urlchange); 
    let info = await response.json(); // читаем ответ в формате JSON
    
    drawinfo()
    getclientinfo(clientid,date);
}

async function change_personal_status(clientid, eventid, status, date){
    urlchange = `http://127.0.0.1:5000/ajax/changestatuspersonal/${clientid}/${eventid}/${status}`;
    
    let response = await fetch(urlchange); 
    let info = await response.json(); // читаем ответ в формате JSON
    
    drawinfo()
    getclientinfo(clientid,date);
}

async function del_personal_event(clientid, eventid, status, date){
    urlchange = `http://127.0.0.1:5000/ajax/delpersonalevent/${clientid}/${eventid}/${status}`;
    
    let response = await fetch(urlchange); 
    let info = await response.json(); // читаем ответ в формате JSON
    
    drawinfo()
    getclientinfo(clientid,date);
}


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
    drawdays();
}//обработка нажатия на предыдущий месяц


let t = document.createElement("div");

function closemodal(){
    let modal = document.querySelector(".ttt");
    modal.classList.remove("show");
    modal.setAttribute("style", "display: none");
    let bodymodal = document.querySelector(".modal-body");
    bodymodal.innerHTML = "";
    t.remove();
    drawinfo();
}// функция закрытия модального окна

function openmodal(clientid, date){
    let modal = document.querySelector(".ttt");
    modal.classList.add("show")
    modal.setAttribute("style", "display: block;");
    
    t.classList.add("modal-backdrop");
    t.classList.add("fade");
    t.classList.add("show");

    document.body.appendChild(t);

    


    let bnt_add_pevent = document.querySelector(".btn_add_pevent")

    console.log(date)
    console.log(clientid)
    console.log(`date in function- ${date}`)
    

    bnt_add_pevent.setAttribute("onclick",`addpevent("${clientid}","${date}")`)

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
            drawinfo();
            getclientinfo(clientid,date);
        }
}


drawdays();




