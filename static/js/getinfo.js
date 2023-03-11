async function getclientinfo(){
    let inn = document.querySelector(".input_inn")
    inn.classList.remove('is-invalid')
    inn.classList.remove('is-valid')

    let responce = await fetch(`/ajax/getinfoinn/?inn=${inn.value}`);
    let info = await responce.json();

    if(!info['error'])
    {

        let name = document.getElementsByName("name")[0];
        let client_fullname = document.getElementsByName("client_fullname")[0];
        let client_shortname = document.getElementsByName("client_shortname")[0];
        let client_uraddress = document.getElementsByName("client_uraddress")[0];
        let client_inn = document.getElementsByName("client_inn")[0];
        let client_kpp = document.getElementsByName("client_kpp")[0];
        let client_ogrn = document.getElementsByName("client_ogrn")[0];
        let client_director = document.getElementsByName("client_director")[0];

        
        name.value = info['short_name'];
        client_fullname.value = info['full_name'];
        client_shortname.value = info['short_name'];
        client_inn.value = info['inn'];
        client_kpp.value = info['kpp'];
        client_ogrn.value = info['ogrn'];
        client_uraddress.value = info['address'];
        client_director.value = info['persone_name'];

        if (info['type'] == "LEGAL"){
            let ul = document.getElementById("radioopf_7");
            ul.checked = true;
        }
        if (info['type'] == "INDIVIDUAL"){
            let ip = document.getElementById("radioopf_8");
            ip.checked = true;
        }
        inn.classList.add('is-valid')
    }
    else{
        inn.classList.add('is-invalid')

    }

    

    
}
