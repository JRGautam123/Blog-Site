const form = document.querySelector("#verifyOtpForm")
const submitBtn = document.getElementById("submitBtn")
const otpInputs = document.querySelectorAll(".otp-input")



// otp handaling

otpInputs.forEach((input, index)=>{
input.addEventListener('input', (e)=>{
        const value = e.target.value
        
        // only allow numbers
        if (!/^\d*/.test(value)){
            e.target.value=""
            return;
        }

        if (value &&  index < otpInputs.length-1){
          
            otpInputs[index + 1].focus()
        }
    }) ;
    // move to the previous input on backspace
    input.addEventListener("keydown", (e) =>{
                                        
        if(e.key === "Backspace" && !input.value && index > 0){
          otpInputs[index-1].focus()

        }
    })
    ;
    
    input.addEventListener('paste', (e) => {
                                      
        e.preventDefault();
        const pasteData = e.clipboardData.getData('text').slice(0, 6)
        if (!/^\d+$/.test(pastedData)) return;

        pastedData.split('').forEach((char, i) => {
        if (otpInputs[i]) {
            otpInputs[i].value = char;
             }
        });
        otpInputs[Math.min(pastedData.length, otpInputs.length - 1)].focus();

  });
});

// form submission

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

const sendOtp = async(data)=>{

    try{
      
        const response = await fetch('/user/verify-otp/',{
            method:'POST',
            headers:{
                "Content-Type": "Application/json",
                "credentials": "include",
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        const result = await response.json()
        return result
    }catch(error){
        console.log(error)
        return null
    }


}


form.addEventListener('submit', async(e) =>{
    e.preventDefault()
    const otp = Array.from(otpInputs).map(input => input.value).join("");
    
    if(otp.length != 6){
        const message =  document.getElementById("alertBox")  
        console.log(message)      
        message.innerText = "Please Enter the complete 6-digit code."
        message.style.color="red"
    }
    data = {
        "otp": otp
    }
   const result = await sendOtp(data)
   console.log(result)
    if(result.success){
        window.location.href = result.redirect_url;
   }
   else if(result.error){
        const rsp =  document.getElementById("alertBox")  
        rsp.innerText = result.error
        rsp.style.color="red"
    }

    
})
                                         
