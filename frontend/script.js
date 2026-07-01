const api="http://localhost:5000";

function loadStudents(){

fetch(api+"/students")

.then(res=>res.json())

.then(data=>{

let rows="";

data.forEach(student=>{

rows+=`

<tr>

<td>${student.id}</td>

<td>${student.name}</td>

<td>${student.email}</td>

<td>${student.course}</td>

<td>

<button onclick="deleteStudent(${student.id})">Delete</button>

</td>

</tr>

`;

});

document.getElementById("table").innerHTML=rows;

});

}

function addStudent(){

fetch(api+"/students",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

name:document.getElementById("name").value,

email:document.getElementById("email").value,

course:document.getElementById("course").value

})

})

.then(()=>loadStudents());

}

function deleteStudent(id){

fetch(api+"/students/"+id,{

method:"DELETE"

})

.then(()=>loadStudents());

}

loadStudents();