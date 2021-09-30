let slideNext = document.querySelector(".slide-next");
let slidePrev = document.querySelector(".slide-prev");

let qnaBox = document.querySelector(".qna-showlist");
let card = document.querySelectorAll(".qna-showcard");
let currentIndex = 0;
let cardCount = card.length;
let cardWidth = 350;
let cardMargin = 50;

qnaBox.style.width = (cardWidth + cardMargin) * cardCount - cardMargin + 'px';


function moveSlide(num) {
    qnaBox.style.left = (-num * 800 + 'px');
    currentIndex = num;
};


slideNext.addEventListener('click', function() {
    if (currentIndex < 2){
        moveSlide(currentIndex + 1);
        console.log(currentIndex);
    } else {
        moveSlide(0);
    }
})

slidePrev.addEventListener('click', function() {
    if (currentIndex > 0){
        moveSlide(currentIndex - 1);
        console.log(currentIndex);
    } else {
        moveSlide(2);
    }
})


 