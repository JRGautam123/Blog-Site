
const sendParentComment=document.querySelector(".send-parent-comment")
var sendChildComment=document.querySelectorAll(".send-child-comment")


const renderParentComment=(response)=>{
     const parentComment= ` <div class="parent-comment d-flex algin-items-center">
                            <div class="user-image">
                                <img src="${response.image}" alt="user-image">
                            </div>
                            <div class="parent-comment-text ms-2">
                                <p class='m-0'>
                                    <a href="" class='text-reset text-decoration-none mx-2' >@${response.user_name}</a>
                                   <strong>${response.date} ago</strong> 
                                </p>
                                <p class='mb-1'>${response.comment}</p>
                              
                               
                                ${response.descendant_count >= 0 ?
                                   `<button class='reply-count-btn${response.comment_id} btn btn-dark rounded-pill mx-2 border-0 ${response.descendant_count === 0 ? 'd-none' : ''}'
                                    data-bs-toggle='collapse' 
                                    data-bs-target="#replied-text-container${response.comment_id}" 
                                    aria-expanded="false"
                                    aria-controls="collapseExample">
    
                                  <span class='reply-count reply-count${response.comment_id} mx-1 my-2'>${response.descendant_count}</span>
                                  ${response.descendant_count == 1 ? "Replies" : "Reply"}
                                </button>` 
                              : ""}

                                
                                    <button class='reply-btn btn btn-dark rounded-pill border-0 my-2 mx-1'
                                            data-bs-toggle='collapse' 
                                            data-bs-target="#form${response.comment_id}"
                                            aria-expanded="false" 
                                            aria-controls="collapseExample">
                                        Reply
                                    </button>
                             
                                <form action="" method='POST'
                                 id="form${response.comment_id}"
                                 class = "collapse w-75">
                                    <div class="form-elemnt d-flex align-items-center">
                                        <textarea name="parent-reply" id="reply-form${response.comment_id}"></textarea>
                                        <i 
                                        class="fa-solid fa-paper-plane ms-2 send-icon send-child-comment"
                                        data-super-parent="${response.comment_id}"
                                        data-parent-id="${response.comment_id}"
                                        data-post-slug="${response.post_slug}"
                                        data-user-id="${response.user_id}"
                                        ></i>
                                    </div>

                                    <p class="text-danger error-text${response.comment_id}"></p>
                                </form>

                            </div>
                        </div> 

                      <hr>
          <div id="replied-text-container${response.comment_id}" class='collapse'>
          </div>
  `
  document.querySelector('.comment-content').insertAdjacentHTML('afterbegin',parentComment)
  document.getElementById('comment').value=""
}

const renderChildComment=(response)=>{
  document.querySelector(`.reply-count-btn${response.super_parent_id}`).classList.remove('d-none')
  console.log(response.super_parent_id)
  
  const descendantCount=document.querySelector(`.reply-count${response.super_parent_id}`)
  descendantCount.innerText=response.descendant_count

  const childComment=`
        <div class="child-comment mx-lg-5 mx-2">
                  <div class='d-flex align-items-start'>
                      <div class="user-image">
                          <img src="${response.image}" alt="">
                      </div>
                      <div class="child-comment-text ms-2">
                          <p class='m-0'>
                              <a href="" class='text-reset text-decoration-none mx-2'>@ ${response.user_name}</a>
                              <strong>${response.date} ago</strong>
                          </p>
                          <p class='mb-1'><strong class='mx-1'>@ ${response.replied_to}</strong>${response.comment}</p>
                         
                          <button class='reply-btn btn btn-dark rounded-pill mx-2 border-0'
                              data-bs-toggle='collapse' 
                              data-bs-target="#form${response.comment_id}" 
                              aria-expanded="false"
                              aria-controls="collapseExample">
                              Reply
                          </button>
                      </div>
                  </div>
                  <form action="" method='POST' id="form${response.comment_id}" class='collapse mt-2 w-50'>
                      <div class="form-elemnt d-flex align-items-center">
                          <textarea name="child-reply" id="reply-form${response.comment_id}"></textarea>
                          <i
                            class="fa-solid fa-paper-plane ms-2 send-icon send-child-comment"
                            data-super-parent="${response.super_parent_id}"
                            data-parent-id="${response.parent_id}"
                            data-post-slug="${response.post_slug}"
                            ></i>
                      </div>
                      <p class="text-danger error-text${response.comment_id}"></p>

                  </form>
                  <hr>
              </div>
  `

  document.getElementById(`replied-text-container${response.super_parent_id}`)
          .insertAdjacentHTML("beforeend",childComment)
  document.getElementById(`reply-form${response.parent_id}`).value=''
  console.log(response.comment_id)

}




const getCookie=(name)=>{
      let cookieValue=null
      if (document.cookie && document.cookie!=="" ){
        const cookies=document.cookie.split(';')
        for(let i =0;i<cookies.length;i++){
          const cookie=cookies[i].trim()
          if(cookie.substring(0,name.length+1)===(name+"=")){
            cookieValue=decodeURIComponent(cookie.substring(name.length+1))
            break
          }

        }
        
      }
      
     return cookieValue 

}





const sendComment=async(url,data)=>{
  try{
    
    const response=await fetch(url,{
      method :'POST',
      headers :{
        'Content-Type':'Application/json',
        'X-CSRFToken':getCookie('csrftoken'),
      },
      body:JSON.stringify(data)
    });
    if(!response.ok){
      
      throw new Error("Failed to send Comment")
    }
    const result=await response.json()
    return result
  }catch(error){
    console.log(error)
    return null
  }

}


const  send=async(url,data)=>{
  const result= await sendComment(url,data)
  if (result){
    if (!result.response.parent_id){
      renderParentComment(result.response)
    }
    else{
      renderChildComment(result.response)
    }
  }
}



const checIfEmpty=(comment)=>{
        if (comment==""){
          
        return true
      }
}


sendParentComment.addEventListener("click",(event)=>{
     const parentComment=document.getElementById('comment').value
     if(checIfEmpty(parentComment)){
        document.querySelector(".error-text").innerText="Please! put your thought"

     }
     else{
       document.querySelector(".error-text").innerText=""
       const postSlug=sendParentComment.dataset.postSlug
       
       const data={
        comment:parentComment,
        post_slug:postSlug,
        parent_id:null

       }

      send(`/${postSlug}/comment`,data)
      
    }

})

let hasClicked = false;
document.querySelector(".comment-content").addEventListener("click",(e)=>{
  if (e.target && e.target.classList.contains('send-child-comment')){
      const parentId=e.target.dataset.parentId


      const childComment= document.getElementById(`reply-form${parentId}`).value
      if(checIfEmpty(childComment)){
        document.querySelector(`.error-text${parentId}`).innerText="Please! put your thought"
      }
      else{
        document.querySelector(`.error-text${parentId}`).innerText=""
        const postSlug=e.target.dataset.postSlug
        const superParent=e.target.dataset.superParent
        

        const data={
          comment:childComment,
          post_slug:postSlug,
          parent_id:parentId,
          super_parent_id:superParent
        }

      

        if (parentId === superParent && !hasClicked) {
          const btn = document.querySelector(`.reply-count-btn${parentId}`);
          if (btn) {
            btn.click();
            hasClicked = true;
          }
        }



        send(`/${postSlug}/comment`,data)
      }
    } 
})
