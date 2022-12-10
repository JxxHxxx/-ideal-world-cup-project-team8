// 전역 변수
let candidate_images = [];
let next_round_images = [];

let now_round_total_matches = 0;
let now_round = 0;

let candidate_images_index = 0;
let next_round_images_index = 0;

let total_matches = 0;


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

           for (let i = 0; i < round_type[0]; i++) {
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
    if (total_matches < round_type[0]) {
        total_matches++
        now_round_total_matches = candidate_images.length/2

        now_round++

        if (idx == 0) {

            next_round_images[next_round_images_index++] = candidate_images[candidate_images_index]
        } else {

            next_round_images[next_round_images_index++] = candidate_images[candidate_images_index + 1]
        }

        if (now_round_total_matches >= 1) {
            candidate_images_index = candidate_images_index + 2

            pick()
        }

        if (now_round_total_matches == now_round) {

            candidate_images = []

            for (let i = 0; i < next_round_images.length; i++) {
                candidate_images[i] = next_round_images[i]
            }

            if (next_round_images.length != 1) {

                next_round_images = []
                candidate_images_index = 0
                next_round_images_index = 0
                now_round = 0
                pick()
            } else {
                document.getElementById("first_image").src = next_round_images[0]

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