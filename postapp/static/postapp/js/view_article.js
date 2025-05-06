document.addEventListener("DOMContentLoaded",()=>{
  const likeIcon=document.querySelector(".like-icon-div"); 
  const likeCount=document.querySelector(".like-count");
  if(likeIcon){
    
        likeIcon.addEventListener("click",async(event)=>{
          event.preventDefault();
          const postSlug=likeIcon.dataset.postSlug;
          const url=`/${postSlug}/like`;
         
          try{
            const response=await fetch(url,{
                method:'POST',
                headers:{
                        'X-CSRFToken':getCookie('csrftoken'),
                        'Accept': 'application/json', 
                },
            });
            if(response.status===401){
              
                window.location.href = `/user/login/?next=${encodeURIComponent(window.location.pathname)}`;
            }

            if(!response.ok){
              
                throw new Error("Like action failed")
            }
            const data=await response.json()
             likeCount.textContent=data.like_count;
            
             likeIcon.classList.toggle("liked",data.user_has_liked)
            
          }
          catch(error){
                console.log(error)
          }

        });
  }

  
  function getCookie(name) {
        let cookieValue = null;
      
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
      
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
      
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
      
        return cookieValue;
      }
      

});