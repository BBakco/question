
//Javascript
var IDBox = document.querySelector('.id-outbox');
var IDInputBox = document.querySelector('#id');
IDInputBox.addEventListener('keyup', function(){
    if(IDInputBox.value !== ''){
        //빈 값이 아닌 경우
        IDBox.classList.add('existence');   
    }else{
        //빈 값인 경우
        IDBox.classList.remove('existence');   
    }
});

var PWBox = document.querySelector('.pw-outbox');
var PWInputBox = document.querySelector('#pw');
PWInputBox.addEventListener('keyup', function(){
    if(PWInputBox.value !== ''){
        //빈 값이 아닌 경우
        PWBox.classList.add('existence');   
    }else{
        //빈 값인 경우
        PWBox.classList.remove('existence');   
    }
});
