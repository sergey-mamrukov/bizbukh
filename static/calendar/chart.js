let d = new Date() 
let y = d.getFullYear();
let m = d.getMonth();

let allevents = []

drawevents();

async function drawevents(){
    url = `http://127.0.0.1:5000/ajax/getallevents`

    let eventrow = document.querySelector(".eventrow")
    
    let response = await fetch(url); 
    let info = await response.json(); // читаем ответ в формате JSON

    

    eventrow.innerHTML = `<td><h4>${getNameMonth(m)}</h4></td>`;//вывод названия месяца в первой ячейке таблицы

    let date = new Date(y,m+1,0);//
    let count_day = date.getDate();//считаем количество дней в месяце

    console.log(date)
  
    for(let i =1; i <= count_day; i++){
        let curdate = dateFormater(new Date(y,m,i))//текущая дата (отформатированная)
        console.log(curdate) 
        for(item in info){
            //&& info[item].type_event == "Отчет"
            if(info[item].dataend == curdate){ 

                eventrow.innerHTML += `<td style="word-wrap:break-word;">
                <div class = "">
                   ${info[item].shortname}
                </div>
                <div>(${info[item].type_event})</div>
                <div class = "text-secondary">${info[item].dataend}</div>
                </td>`;


                allevents.push(info[item])
            }   
        }
    }




    let dateinfo = document.querySelector(".dateinfo");
    dateinfo.textContent =  `${getNameMonth(m)} - ${y} года`;//вывод информации в хлебных крошках
    drawinfo();
    changeButtonName()//вызов функции смены названия кнопок предыдущего и следующео месяца 
    

}



async function drawinfo(){
    url = `http://127.0.0.1:5000/ajax/get`

    let response = await fetch(url); 
    let info = await response.json(); // читаем ответ в формате JSON


    // let date = new Date(y,m+1,0);
    // let count_day = date.getDate();
    let tbody = document.querySelector(".info");
    // console.log(date)

    tbody.innerHTML = "";//обнуляем таблицу для перерисовки данных


    for(item in info){
        let client_info = document.createElement("tr");

        client_info.innerHTML += 
        `<td class = "text-light bg-secondary p-3">
        <a class = "text-light" href = "http://127.0.0.1:5000/client/${info[item].client_id}">${info[item].clientname}</a>
        </td>`;

        let clientevents = info[item].events
        let actual = []

        // for (el in clientevents){
        //     // console.log(`el - ${clienntevents[el].eventid}`)
        //     for(e in allevents){
        //         if(clientevents[el].eventid == allevents[e].eventid){
        //             actual.push(clientevents[el])
        //         }
        //     }
           
        // }

        for (e in allevents){
            for(el in clientevents){
                if(clientevents[el].eventid == allevents[e].eventid){
                    actual.push(clientevents[el])
                }
            }
           
        }
        console.log(`-----------------${getNameMonth(m)}---${info[item].clientname}-----------------------`)
        console.log(`actual ${actual}`)
        console.log(`clientevents ${clientevents}`)
        console.log(`allevents ${allevents}`)
        console.log(`-------------------------------------------`)
       
        for(e in allevents){
            let nullcol = true;

            for(a in actual){ 
                if(allevents[e].eventid == actual[a].eventid){
                    if(actual[a].status == "Подтверждено"){
                        client_info.innerHTML += `<td class = "bg-success text-light">${actual[a].status}</td>`;
                    }
                    if(actual[a].status == "Выполнено"){
                        client_info.innerHTML += `<td class = "bg-warning text-light">${actual[a].status}</td>`;
                    }
                    if(actual[a].status == "Не выполнено"){
                        client_info.innerHTML += `<td class = "bg-info text-light">${actual[a].status}</td>`;
                    }

                    if(actual[a].status == "None"){
                        client_info.innerHTML += `<td class = "bg-info text-light">Не выполнено<br>${actual[a].status}</td>`;
                    }
                    nullcol= false
                }
            }

            if(nullcol){
                client_info.innerHTML += `<td class = "bg-light text-secondary"> </td>`;
            }
        }


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