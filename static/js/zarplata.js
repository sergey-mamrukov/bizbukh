const urlajax = `http://127.0.0.1:5000`;
let d = new Date()
let y = d.getFullYear();
let m = d.getMonth();
/// берем сегодняшнюю дату

let client_id = Number(document.querySelector(".clientid").textContent);

let plug = `
<div class = "card">
    <div class = "card-body">
        <div class = "alert alert-success" role="alert">Задачи по зарплате и авансу сформированы</div>

        <div class = "text-center p-4 m-4">
        <a class = "btn btn-outline-primary" href = "/client">Перейти к списку организаций</a>
        <a class = "btn btn-outline-primary" href = "/client/${client_id}">Перейти в карточку организации</a>
        <a class = "btn btn-outline-primary" href = "/client/clientedit/${client_id}">Перейти к редактированию организации</a>
        </div> 
    </div>
</div>
`;

let place = document.querySelector(".place");

let tablecol = document.querySelector(".tablecol");
let settingscol = document.querySelector(".settingscol");


let tablebody = document.querySelector(".table-body");

let selectyear = document.createElement("select");
selectyear.className = "form-select";


let select_year = document.querySelector(".select-year");
select_year.appendChild(selectyear);

let yearnow = document.createElement("option");
yearnow.value = `${y}`;
yearnow.textContent = `${y}`;
yearnow.checked = true;

let yearnext = document.createElement("option");
yearnext.value = `${y + 1}`;
yearnext.textContent = `${y + 1}`;

selectyear.appendChild(yearnow)
selectyear.appendChild(yearnext)



for (let i = 0; i < 12; i++) {
    let tr = document.createElement("tr");

    let namemonth = document.createElement("td");
    namemonth.innerHTML = getNameMonth(i);

    let dataavansa = document.createElement("td");
    let datazp = document.createElement("td");



    let select_day_avans = document.createElement("select");
    select_day_avans.classList.add("form-select");
    select_day_avans.id = `avans-${y}-${i + 1}`;
    select_day_avans.addEventListener("change", checkweekend)



    let select_day_zp = document.createElement("select");
    select_day_zp.classList.add("form-select");
    select_day_zp.id = `zp-${y}-${i + 1}`;
    select_day_zp.addEventListener("change", checkweekend)


    let date = new Date(y, i + 1, 0);//
    let count_day = date.getDate();//считаем количество дней в месяце

    for (let j = 1; j <= count_day; j++) {
        let t = getWeekDay(new Date(y, i, j - 1).getDay())//заполняем строчку днями
        let option = document.createElement("option")
        option.value = j;
        option.textContent = `${j} (${t})`;
        select_day_avans.appendChild(option)
    }

    for (let j = 1; j <= count_day; j++) {
        let t = getWeekDay(new Date(y, i, j - 1).getDay())//заполняем строчку днями
        let option = document.createElement("option")
        option.value = j;
        option.textContent = `${j} (${t})`;
        select_day_zp.appendChild(option)
    }

    dataavansa.appendChild(select_day_avans);
    datazp.appendChild(select_day_zp);

    tr.appendChild(namemonth);
    tr.appendChild(dataavansa);
    tr.appendChild(datazp);

    tablebody.appendChild(tr)
}


async function result() {
    
    let result_avans = [];
    for (let i = 1; i <= 12; i++) {
        let select = document.getElementById(`avans-${y}-${i}`)
        let date = new Date(selectyear.value, i - 1, select.value)
        result_avans.push(dateFormater(date))
    }
    console.log("data avansa: " + result_avans)

    let result_zp = [];
    for (let i = 1; i <= 12; i++) {
        let select = document.getElementById(`zp-${y}-${i}`)
        let date = new Date(selectyear.value, i - 1, select.value)
        result_zp.push(dateFormater(date))
    }
    console.log("data zp: " + result_zp)


    result = [];


    for(r in result_avans){
        result.push({
            "client_id":client_id,
            "data":result_avans[r],
            "name":"Выплата аванса",
            "shortname":"Аванс",
        })
    }

    for(r in result_zp){
        result.push({
            "client_id":client_id,
            "data":result_zp[r],
            "name":"Выплата заплаты",
            "shortname":"Заплата",
        })
    }

    console.log(result)
    let responce = await fetch("http://127.00.1:5000/ajax/addzpevent/", { method: 'POST', body: JSON.stringify(result) });
    let info = await responce.json()
   

    if(info['status_add'] == 'ok'){
        tablecol.remove()
        settingscol.remove()
        place.innerHTML = plug;
    }
}




function fillday() {
    let dayavans = document.querySelector(".day-avans");
    let dayzp = document.querySelector(".day-zp");

    console.log(dayavans)
    console.log(dayzp)


    for (let i = 1; i <= 12; i++) {
        let date = new Date(selectyear.value, i, 0);//
        let count_day = date.getDate();//считаем количество дней в месяце

        let select = document.getElementById(`avans-${y}-${i}`)
        if (Number.isInteger(Number(dayavans.value)) && Number(dayavans.value) >= 1) {
            if (dayavans.value > count_day) select.value = count_day
            else select.value = dayavans.value
        }
        else {
            select.value = 1
        }

    }

    for (let i = 1; i <= 12; i++) {
        let date = new Date(y, i, 0);//
        let count_day = date.getDate();//считаем количество дней в месяце



        let select = document.getElementById(`zp-${y}-${i}`)
        if (Number.isInteger(Number(dayzp.value)) && Number(dayzp.value) >= 1) {
            if (dayzp.value > count_day) select.value = count_day
            else select.value = dayzp.value
        }
        else {
            select.value = 1
        }
    }

    checkweekend()

}

function checkweekend() {
    let allselect = document.querySelectorAll("select")
    console.log(allselect[0].selectedOptions[0].text)
    console.log(allselect[0].text)
    for (let i = 0; i <= allselect.length; i++) {

        if (allselect[i].selectedOptions[0].text.includes("Сб") || allselect[i].selectedOptions[0].text.includes("Вс")) {
            allselect[i].classList.add("is-invalid")
        }
        else allselect[i].classList.remove("is-invalid")
    }


}






function getWeekDay(dayNumber) {
    switch (dayNumber + 1) {
        case 7: return "Вс";
        case 1: return "Пн";
        case 2: return "Вт";
        case 3: return "Ср";
        case 4: return "Чт";
        case 5: return "Пт";
        case 6: return "Сб";
    }
}//возвращает название дней недели

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