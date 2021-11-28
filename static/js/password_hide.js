const pswrdField = document.querySelector(".input[type='password']"),

toggleIcon = document.getElementById("pw");
console.log(pswrdField,toggleIcon)


toggleIcon.onclick = () =>{
  console.log("show")
  if(pswrdField.type === "password"){
    pswrdField.type = "text";
    toggleIcon.classList.add("active");
  }else{
    pswrdField.type = "password";
    toggleIcon.classList.remove("active");
  }
}
