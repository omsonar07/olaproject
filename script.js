function showPage(page){
    document.querySelectorAll('.page').forEach(p => p.style.display="none");
    document.getElementById(page).style.display="block";
}

/* REGISTER */
function registerUser(){
    fetch("/register", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({
            name: rname.value,
            email: remail.value,
            mobile: rmobile.value,
            password: rpass.value
        })
    })
    .then(res=>res.json())
    .then(data=>{
        alert(data.message || data.error);
        showPage('login');
    });
}

/* LOGIN */
function loginUser(){
    fetch("/login", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({
            mobile: loginMobile.value,
            password: loginPass.value
        })
    })
    .then(res=>res.json())
    .then(data=>{
        if(data.user){
            alert("Login Success");
            loadProfile(data.user);
            showPage('home');
        }else{
            alert(data.error);
        }
    });
}

/* PROFILE */
function loadProfile(user){
    pname.innerText = "Name: " + user.name;
    pemail.innerText = "Email: " + user.email;
    pmobile.innerText = "Mobile: " + user.mobile;
}

/* FEEDBACK */
function submitFeedback(){
    fetch("/feedback", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({
            name: fname.value,
            rating: rating.value,
            message: message.value
        })
    })
    .then(res=>res.json())
    .then(data=>{
        alert(data.message);
    });
}

function viewFeedback(){
    fetch("/feedback")
    .then(res=>res.json())
    .then(list=>{
        let output="";
        list.forEach(f=>{
            output+=`
            <div style="background:#00000080;padding:10px;margin:5px;">
                <b>${f.name}</b><br>
                ${f.rating}<br>
                ${f.message}
            </div>`;
        });
        feedbackList.innerHTML=output;
    });
}

showPage('home');
