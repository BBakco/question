	<!--비밀번호 변경-->
	
	<!--로그아웃 알림 로그아웃-->        
    function confirmLogout() {
        if( confirm("로그아웃 하시겠습니까?") ) {
            location.href = "<c:url value ='/member/logout'/>";
        }
    }
	<!--infinite paging->
	const io = new IntersectionObserver((entries, observer) => {
	entries.forEach(entry => {
	  if (!entry.isIntersecting) return; 
		
	  if (page._scrollchk) return;
		
    observer.observe(document.getElementById('sentinel'));
		
    page._page += 1;
		
    page.list.search();
		.
	});
});

io.observe(document.getElementById('sentinel'));
		
		$.ajax({
	url: url,
	data: param,
	method: "GET",
	dataType: "json",
	success: function (result) {
	  console.log(result);
	},
	error: function (err) {
	  console.log(err);
	},
	beforeSend: function () {
    _scrollchk = true; 
		
		document.getElementById('list').appendChild(skeleton.show());
    $(".loading").show();
	},
	complete: function () {
    _scrollchk = false;
		$(".loading").hide();
    skeleton.hide();
		
	}
});
