// 전역 변수
let candidate_images = [];
let next_round_images = [];

let now_round_total_matches = 0;
let now_round = 0;

let candidate_images_index = 0;
let next_round_images_index = 0;

let final = 0;

function read_result() {
    $.ajax({
        type: 'GET',
        url: '/api/noodle/read',
        data:{},
        success: function (response) {
            ideal_list = response['ideal']
            console.log(ideal_list)
            for (let i = 0; i < ideal_list.length; i++) {

                let result_html = `<tr>
                                      <td>${ideal_list[i]['name']}</td>     
                                      <td>${ideal_list[i]['win']}</td>     
                                    </tr>`

                $('#result-box').append(result_html)
            }
        }
    })
}

function add_noodle() {
    $.ajax({
       type: 'GET',
       url: '/api/noodle/read',
       data: {},
       success: function (response) {
           ideal_list = response['ideal']

           for (let i = 0; i < 4; i++) {
                candidate_images[i] = ideal_list[i]['img']
           }
           pick()
       }
    })
}

function pick() {
    document.getElementById('first_image').src=candidate_images[candidate_images_index]
    document.getElementById('second_image').src=candidate_images[candidate_images_index + 1]
}

function change(idx) {
    if (final < 4) {
        final++
        now_round_total_matches = candidate_images.length/2
        console.log("Round " + candidate_images_index/2)
        console.log("이번 " +candidate_images.length + "강의 매치 횟수 " + now_round_total_matches)
        now_round++

        if (idx == 0) {
            console.log("왼쪽을 선택하셨습니다.")
            next_round_images[next_round_images_index++] = candidate_images[candidate_images_index]
        } else {
            console.log("오른쪽을 선택하셨습니다.")
            next_round_images[next_round_images_index++] = candidate_images[candidate_images_index + 1]
        }

        if (now_round_total_matches >= 1) {
            candidate_images_index = candidate_images_index + 2
            console.log("다음 경기를 준비합니다.")
            pick()
        }

        if (now_round_total_matches == now_round) {
            console.log(candidate_images.length + "강 매치가 끝났습니다.")
            candidate_images = []

            for (let i = 0; i < next_round_images.length; i++) {
                candidate_images[i] = next_round_images[i]
            }

            if (next_round_images.length != 1) {
                next_round_images = []
                candidate_images_index = 0
                next_round_images_index = 0
                now_round = 0
                console.log("다음 매치를 위한 초기화 작업이 종료되었습니다.")
                pick()
            } else {
                document.getElementById("first_image").src = next_round_images[0]
                //최종 결과는 한장으로 나오게

                // let result_html = `<button onclick="send_result()">결과 보기</button>`
                let result_html = `<button onclick="location.href='select/result'; save_result()">결과 보기</button>`
                $('#result').append(result_html)

            }
        }
    }
}

function save_result() {
    let result_img = next_round_images[0]
    $.ajax ({
        type: 'POST',
        url: "/api/noodle/save",
        data:{img_give:result_img},
        success : function (response) {
        }
    })
}