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
                let noodle_name = ideal_list[i]['name']
                let noodle_img = ideal_list[i]['img']
                let noodle_win =ideal_list[i]['win']

                let result_html = `<tr>
                                      <td>${i+1}등</td>  
                                      <td><img src="${noodle_img}" width=100 height=100></td>
                                      <td>${noodle_name}</td> 
                                      <td><a onclick="location.href='/select/detail/${noodle_name}'")" >${noodle_win}</a></td>     
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
           shuffle(candidate_images)
           pick()
       }
    })
}

function shuffle(array) {
  array.sort(() => Math.random() - 0.5);
}

function show_round_info() {
    if ((candidate_images.length) > 2) {
        const element = document.getElementById('now-round');
        element.innerText = candidate_images.length + "강 " +  (now_round+1) + "/" + candidate_images.length/2
    } else {
        const element = document.getElementById('now-round');
        element.innerText = "결승전"
    }
}

function pick() {

    document.getElementById('first_image').src=candidate_images[candidate_images_index]
    document.getElementById('second_image').src=candidate_images[candidate_images_index + 1]

    show_round_info()

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

            shuffle(candidate_images)

            if (next_round_images.length != 1) {

                next_round_images = []
                candidate_images_index = 0
                next_round_images_index = 0
                now_round = 0
                pick()

            } else {
                document.getElementById("first_image").src = next_round_images[0]

                let result_html = `<button class="btn btn-success" onclick="location.href='select/result'; save_result()">결과 보기</button>`
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

function get_nick() {
    $.ajax ({
        type:'GET',
        url: "/api/nick",
        data:{},
        success : function (response) {

            let temp_html = `<h1>${response}님은 어떤 라면을 좋아하시나요?</h1>`

            $('#noodle-title').append(temp_html)
        }
    })
}

// function temp_hide() {
//     $('img.first').click( function () {
//             $('img.second').hide(1000, function () {
//                 $(this).show()
//             });
//                })
//
//     $('img.second').click( function () {
//             $('img.first').hide(1000, function () {
//                 $(this).show()
//             });
//                })
// }