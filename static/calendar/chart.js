let d = new Date() 
let y = d.getFullYear();
let m = d.getMonth();

let allevents = []

let spinner = document.createElement('div');
    spinner.classList.add('spinner-border','position-absolute','top-50','start-50');
    spinner.setAttribute("role","status");

let cardbody = document.querySelector(".cardbody");

changeButtonName();
drawevents();

async function drawevents(){
    url = `http://127.0.0.1:5000/ajax/getallevents`
    cardbody.appendChild(spinner);

    let eventrow = document.querySelector(".eventrow")

    
    let response = await fetch(url); 
    let info = await response.json(); // читаем ответ в формате JSON

    if(info.length == 0){ 
        spinner.remove();
        cardbody.innerHTML = `
        <div class="alert border-0 bg-danger alert-dismissible fade show py-2">
            <div class="d-flex align-items-center">
                <div class="fs-3 text-light-danger"><i class="bi bi-exclamation-triangle-fill"></i></div>
                <div class="ms-3">
                    <div class="text-light">Недостаточно данных. Добавьте компанию или измените параметры компании</div>
                </div>
            </div>
      </div>`
        return;
    }

    eventrow.innerHTML = `<td class = "border col-3" ><h4>${getNameMonth(m)}</h4></td>`;//вывод названия месяца в первой ячейке таблицы

    let date = new Date(y,m+1,0);//
    let count_day = date.getDate();//считаем количество дней в месяце

    // console.log(date)
  
    for(let i =1; i <= count_day; i++){
        let curdate = dateFormater(new Date(y,m,i))//текущая дата (отформатированная)
        
        for(item in info){
          
            if(info[item].dataend == curdate){ 

                eventrow.innerHTML += `<td class = "border col-2 align-bottom">
                
                <a  href = "http://127.0.0.1:5000/calendar/change/${info[item].eventid}"> ${info[item].shortname}</a>
                <br>
                
                (${info[item].type_event})
                <div class = "text-secondary">${info[item].dataend}</div>
                </td>`;

                allevents.push(info[item])
            }   
        }
    }

    spinner.remove()


    let dateinfo = document.querySelector(".dateinfo");
    dateinfo.textContent =  `на ${getNameMonth(m)} - ${y} года`;//вывод информации в хлебных крошках
    drawinfo();
    changeButtonName()//вызов функции смены названия кнопок предыдущего и следующео месяца 
    

}



async function drawinfo(){
    url = `http://127.0.0.1:5000/ajax/get`

    cardbody.appendChild(spinner);

    let response = await fetch(url); 
    let info = await response.json(); // читаем ответ в формате JSON

    let tbody = document.querySelector(".info");


    tbody.innerHTML = "";//обнуляем таблицу для перерисовки данных


    for(item in info){
        let client_info = document.createElement("tr");
        client_info.classList.add("d-flex")

        client_info.innerHTML += 
        `<td class = "col-3 text-light bg-secondary p-3">
        <a class = "text-light" style = "" href = "http://127.0.0.1:5000/client/${info[item].client_id}">${info[item].clientname}</a>
        
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
        // console.log(`-----------------${getNameMonth(m)}---${info[item].clientname}-----------------------`)
        // console.log(`actual ${actual}`)
        // console.log(`clientevents ${clientevents}`)
        // console.log(`allevents ${allevents}`)
        // console.log(`-------------------------------------------`)
        
        console.log(allevents)

        for(e in allevents){
            let nullcol = true;

          

            for(a in actual){ 
                if(allevents[e].eventid == actual[a].eventid){
                    if(actual[a].status == "Подтверждено"){
                        client_info.innerHTML += `<td class = "border col-2 bg-success text-light">Подтверждено</td>`;
                    }
                    if(actual[a].status == "Выполнено"){
                        client_info.innerHTML += `<td class = "border col-2 bg-success-subtle text-secondary">Выполнено</td>`;
                    }
                    if(actual[a].status == "Не выполнено"){
                        client_info.innerHTML += `<td class = "border col-2 bg-danger-subtle text-secondary">Не выполнено</td>`;
                    }

                    if(actual[a].status == "Не выполняется"){
                        client_info.innerHTML += `<td class = "border col-2 bg-dark-subtle text-secondary">Не выполняется</td>`;
                    }

                    if(actual[a].status == "None"){
                        client_info.innerHTML += `<td class = "border col-2 bg-danger-subtle text-secondary">Не выполнено</td>`;
                        // ${actual[a].status}
                    }

                    // console.log(info[item].clientname)
                    // console.log(allevents[e].dataend)
                    // console.log(`${y}-${m}-${info[item].dataavansa}`)


                    
                    nullcol= false
                }



            
            }

            // if(allevents[e].dataend == info[item].dataavansa && allevents[e].shortname == "Аванс"){
            //     client_info.innerHTML += `<td class = "bg-info text-light">${actual[a].status}</td>`;
            //     // console.log(info[item].clientname)
            //     nullcol= false
            // }

            // if(allevents[e].dataend == info[item].datazp && allevents[e].shortname == "Зарплата"){
            //     client_info.innerHTML += `<td class = "bg-info text-light">${actual[a].status}</td>`;
            //     // console.log(info[item].clientname)
            //     nullcol= false
            // }

            if(nullcol){
                client_info.innerHTML += `<td class = "border col-2 bg-light text-secondary"> </td>`;
            }
        }

        spinner.remove();
        tbody.appendChild(client_info);
    }
    
}//вывод информации в таблицу










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