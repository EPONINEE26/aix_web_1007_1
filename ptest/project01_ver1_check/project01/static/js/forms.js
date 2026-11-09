// 파일 경로: static/js/forms.js
// 수정: 기존 fetch + async/await 방식 코드 전체 삭제 후 jQuery 의 $.ajax 방식으로 교체
//
// [이 파일의 역할]
// - base.html 맨 아래에서 불러오는 파일 (그래서 모든 페이지에서 동작)
// - <form data-ajax> 라고 적힌 폼(로그인, 글쓰기, 글수정, 답글, 글삭제, 댓글 등록/수정/삭제)의 전송 담당
// - 기본 폼 전송 = 버튼 클릭 시 화면 전체가 새로고침되며 이동
// - $.ajax 전송 = 화면 새로고침 없이 뒤에서 서버에 데이터 전송 후 결과만 받아오는 방식
//
// [용어 설명]
// - jQuery : 자바스크립트를 짧게 쓰게 해주는 도구 모음 (base.html 에서 먼저 불러온 상태)
// - $ 기호 : jQuery 를 사용한다는 표시
// - 함수(function) : 여러 줄의 코드에 이름을 붙여 묶어 둔 것, 필요할 때 실행
// - 변수(var) : 값을 잠시 담아 두는 상자

// 추가: 폼이 전송(submit)될 때 아래 함수를 실행하는 설정
// - $(document).on("submit", "form[data-ajax]", 함수) = 페이지 안의 모든 폼 중 data-ajax 가 붙은 폼에서 전송 이벤트 발생 시 함수 실행
// - function (event) 의 event = 방금 일어난 전송 동작에 대한 정보
$(document).on("submit", "form[data-ajax]", function (event) {

    // 추가: 폼의 원래 동작(화면 새로고침 이동) 차단
    // - 차단 이유 = 아래의 $.ajax 로 대신 전송하기 위함
    event.preventDefault();

    // 추가: 지금 전송된 폼을 변수 form 에 보관
    // - this = 지금 전송된 폼 자신
    var form = $(this);

    // 추가: 그 폼 안의 전송 버튼을 변수 submitButton 에 보관
    // - 보관 이유 = 전송 중 버튼 잠금(여러 번 눌러 중복 전송되는 문제 방지)
    var submitButton = form.find("button[type=submit]");

    // 추가: 이미 전송 중인지 검사
    // - if (조건) { } = 조건이 맞을 때만 중괄호 안 코드 실행
    // - return = 함수를 여기서 즉시 종료 (아래 코드 실행 안 함)
    if (form.data("submitting") === true) {
        return;
    }

    // 추가: 폼에 적힌 data-confirm 문구(예: "삭제하시겠습니까?") 가져오기
    var confirmation = form.attr("data-confirm");

    // 추가: 문구가 있으면 확인/취소 창 표시, 취소를 누르면 전송 중단
    // - confirm("문구") = 확인 누르면 true, 취소 누르면 false
    // - ! 기호 = 반대로 뒤집는 기호 (취소를 눌렀을 때 조건 성립)
    if (confirmation && !confirm(confirmation)) {
        return;
    }

    // 추가: 전송 시작 표시 + 버튼 잠금
    // - 전송이 끝나면 아래 ajaxComplete 함수에서 원래대로 복구
    form.data("submitting", true);
    submitButton.prop("disabled", true);

    // 추가: 서버가 정상 답변을 줬을 때 실행할 함수
    // - data = 서버가 보내준 답변 (예: 이동할 주소가 들어 있음)
    function ajaxSuccess(data) {
        // 답변에 이동 주소가 없는 경우의 안내
        if (!data.redirect_url) {
            alert("서버 응답에서 이동할 주소를 찾지 못했습니다.");   // alert = 알림창 표시
            return;
        }
        // 로그인 폼일 때만 로그인 완료 안내
        // - indexOf = 글자 안에서 특정 글자의 위치 찾기, 없으면 -1
        if (form.attr("action").indexOf("/member/login/") !== -1) {
            alert("로그인이 되었습니다.");
        }
        // 서버가 알려준 주소로 화면 이동
        location.href = data.redirect_url;
    }

    // 추가: 서버가 오류 답변을 줬을 때 실행할 함수
    // - xhr = 서버의 오류 답변에 대한 정보 (xhr.status = 오류 번호)
    function ajaxError(xhr) {
        // 기본 안내 문구
        var message = "요청을 처리하지 못했습니다. 입력값과 서버 상태를 확인해 주세요.";
        // 오류 번호 403 = 권한 없음 또는 로그인 시간 만료
        if (xhr.status === 403) {
            message = "요청을 처리할 권한이 없거나 세션이 만료되었습니다.";
        }
        // 서버가 직접 보낸 안내 문구(message)가 있으면 그 문구로 교체
        if (xhr.responseJSON && xhr.responseJSON.message) {
            message = xhr.responseJSON.message;
        }
        alert(message);
    }

    // 추가: 성공/실패와 관계없이 마지막에 실행할 함수
    // - 전송 중 표시 해제 + 버튼 잠금 해제
    function ajaxComplete() {
        form.data("submitting", false);
        submitButton.prop("disabled", false);
    }

    // 추가: 폼 안에 파일 선택칸(input type=file)이 있는지 검사
    // - 있는 폼 = 글쓰기, 글수정, 답글 (첨부파일 전송 필요)
    // - length > 0 = 찾은 개수가 1개 이상
    if (form.find("input[type=file]").length > 0) {

        // 추가: 파일이 있는 폼의 $.ajax 전송
        // - $.ajax({ ... }) = 화면 이동 없이 서버와 데이터를 주고받는 jQuery 기능
        $.ajax({
            url: form.attr("action"),        // 데이터를 보낼 서버 주소 (폼의 action 에 적힌 주소)
            type: "post",                    // 전송 방식 (post = 주소창에 값을 드러내지 않고 보내는 방식)
            data: new FormData(this),        // 보낼 데이터 (입력값 + 파일 + 보안 확인 번호를 한 묶음으로 만든 것)
            processData: false,              // 데이터를 jQuery 가 글자로 바꾸지 못하도록 막는 설정 (파일 전송에 필수)
            contentType: false,              // 파일 전송용 형식 표시를 브라우저가 자동으로 붙이도록 하는 설정 (파일 전송에 필수)
            dataType: "json",                // 서버 답변의 형식 (json = 글자로 된 데이터 묶음)
            success: ajaxSuccess,            // 정상 답변 시 실행할 함수 (위에서 만든 함수)
            error: ajaxError,                // 오류 답변 시 실행할 함수 (위에서 만든 함수)
            complete: ajaxComplete           // 끝난 뒤 항상 실행할 함수 (위에서 만든 함수)
        });

    } else {

        // 추가: 파일이 없는 폼(로그인, 삭제, 댓글)의 $.ajax 전송
        $.ajax({
            url: form.attr("action"),        // 데이터를 보낼 서버 주소 (폼의 action 에 적힌 주소)
            type: "post",                    // 전송 방식 (post)
            data: form.serialize(),          // 보낼 데이터 (폼 안의 입력값을 "이름=값&이름=값" 형태로 묶은 것, 보안 확인 번호 포함)
            dataType: "json",                // 서버 답변의 형식 (json)
            success: ajaxSuccess,            // 정상 답변 시 실행할 함수
            error: ajaxError,                // 오류 답변 시 실행할 함수
            complete: ajaxComplete           // 끝난 뒤 항상 실행할 함수
        });

    }
});
