a=document.querySelectorAll('.check')
var check = []


for (var j = 1; j<a.length; j++){
    check.push(a[j])
    j=j+1;
}
let Checked = null;
//The class name can vary
for (let CheckBox of check){
    
	CheckBox.onclick = function(){
  	if(Checked!=null){
      Checked.checked = false;
      Checked = CheckBox;
    }
    Checked = CheckBox;
    var search=(CheckBox.getAttribute("id"))
    var a =search.split(",")[3]
    document.getElementById("cedula").value = a.split(" ")[1];
    if(Checked.checked == false){
        document.getElementById("cedula").value =null;
    }

  }
}



document.addEventListener('DOMContentLoaded', () => {
            
    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    
    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {
    
    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
        el.addEventListener('click', () => {
    
        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);
    
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');
    
        });
    });
    }
    
    });

    


document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        const $notification = $delete.parentNode;

        $delete.addEventListener('click', () => {
        $notification.parentNode.removeChild($notification);
        });
    });
    });

