<!--로그아웃 알림, 로그아웃 -->
 function confirmLogout() {
        if( confirm("정말 로그아웃 하시겠습니까?") ) {
            location.href = "<c:url value ='/member/logout'/>";
        }
    }
<!--내가 쓴 글 -->
function showmyqna() {
	$ajax({
		type: "GET",
		url: "/myqna",
		data:{},
		success: function (response){
			let myqnas = response['all_myqnas']
			for(let i = 0; i < myqnas.lenght; i++) {
				let question = myqnas[i]['question']
				let answer = myqnas[i]['answer']
				
				let temp_html = `<div id="QnA" class="myqna">
					<div class="cardlist" href="">
						<p id="Question" class="question">Q.${question}
						<p id="Answer" class="answer">A.${answer}`
				$('#QnA').append(temp_html)
				}
			}
		})
	}

<!--다른사람이 쓴 글-->

<!--탈퇴하기-->

function del() {
	swal({
		title: "정말 탈퇴하시겠습니까?",
		text: "한번 탈퇴하시면 회원정보를 다시 복구할 수 없습니다!",
		icon: "warning",
		buttons: true,
		dangerMode: true,
	})
	.then((willDelete) => {
		if (willDelete) {
			location.href='/member/out'
		} else {
			swal("탈퇴처리가 취소되었습니다.");
			}
	});
};
