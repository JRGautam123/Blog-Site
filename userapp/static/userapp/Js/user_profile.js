const editProfile=document.querySelectorAll(".edit-profile");
const updateBtn=document.querySelector('.update-btn')

// making the form field disabled initally.

var disableEnableFields = (status ) => {
    const fields = document.querySelectorAll("#id_username, #id_first_name, #id_last_name, #id_email, #id_image");
    fields.forEach(field => {
        field.disabled = status;
    });
}


document.addEventListener("DOMContentLoaded", (event) => {
    disableEnableFields(true); 
});







editProfile.forEach(element => {
    element.addEventListener('click',()=>{
        if (updateBtn.classList.contains("update")){
            updateBtn.classList.remove("update")
            updateBtn.classList.add('updatebtn-added')
            disableEnableFields(false)
        }
        else{
            updateBtn.classList.remove("updatebtn-added")
            updateBtn.classList.add("update")
            disableEnableFields(true)
        }
      
    })  
});

