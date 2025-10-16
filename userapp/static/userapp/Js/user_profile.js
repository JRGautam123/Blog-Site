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

// adding backgound effect in user profile manipulation options 

const items = document.querySelectorAll(".options-on-lg li");
const itemList=[...items]
var clicked_item=0
itemList.forEach((item,idx)=>{
  item.addEventListener('click',(event)=>{
    
    if (item.classList.contains('edit-profile') && item.classList.contains('clicked-li')){
        item.classList.remove('clicked-li')
        itemList[0].classList.add('clicked-li')
        clicked_item=0
    }
    else{
        itemList[clicked_item].classList.remove('clicked-li')
        item.classList.add('clicked-li')
        clicked_item=idx
        
    }
  })
})
// toggling on small screen

const itemOnSm=document.querySelectorAll(".options-on-sm li")
const closeBtn=document.querySelector(".btn-close")
itemOnSm.forEach(item=>item.addEventListener('click',()=>{
  
    closeBtn.click()
}))
