var course_name;
var college_name;
var category_name;
var district_name;
var reservation_category;

document.getElementById("id_category").addEventListener("change", function (e) {
    category_name = this.value;
    get_courses(category_name);
    get_districts(category_name, course_name);
    get_colleges(category_name, course_name, district_name);
})

document.getElementById("id_course").addEventListener("change", function (e) {
    course_name = this.value;
    get_districts(category_name, course_name);
    get_colleges($("#id_category").value, course_name, district_name);
})

document.getElementById("id_district").addEventListener("change", function (e) {
    district_name = this.value;
    get_colleges(category_name, course_name, district_name);
})

document.getElementById("id_college").addEventListener("change", function (e) {
    college_name = this.value;

    get_seat_matrix(course_name, college_name, reservation_category);
})


document.getElementById("id_reservation").addEventListener("change", function (e) {
    reservation_category = this.value;
    get_seat_matrix(course_name, college_name, reservation_category);
})

function get_courses(category_name) {
    $.post(
        "seat-finder/ajax/get-courses",
        {
            "category_name": category_name
        },
        function (data, status) {
            var courses = data["courses"];
            $("#id_course").empty();
            $("#id_course").prepend("<option>--select--</option>");
            courses.forEach(element => {

                $("#id_course").prepend(
                    `<option value="${element}">${element}</option>`
                )
            });
        }
    )
}


function get_districts(category_name, course_name) {
    $.post(
        "seat-finder/ajax/get-districts",
        {
            "category_name": category_name,
            "course_name": course_name
        },
        function (data, status) {

            var districts = data["districts"];
            $("#id_district").empty();
            $("#id_district").prepend("<option>--select--</option>");
            districts.forEach(element => {
                $("#id_district").prepend(
                    `<option value="${element}">${element}</option>`
                )
            });

        }
    )
}

function get_colleges(category_name, course_name, district_name) {
    $.post(
        "seat-finder/ajax/get-colleges",
        {
            "category_name": category_name,
            "course_name": course_name,
            "district_name": district_name
        },
        function (data, status) {

            var colleges = data["colleges"];
            $("#id_college").empty();
            $("#id_college").prepend("<option>--select--</option>");
            colleges.forEach(element => {
                $("#id_college").prepend(
                    `<option value="${element}">${element}</option>`
                )
            });

        }
    )
}


function get_seat_matrix(course_name, college_name, reservation_category) {
    if (reservation_category === undefined) {
        
    } else {
        $.post(
            "seat-finder/ajax/get-seat-matrix",
            {
                "college_name": college_name,
                "course_name": course_name,
                "reservation_category": reservation_category
            },
            function (data, status) {
                var seat_matrix_data = data["seat_matrix_data"];
                $("#id_seat_matrix_table").empty();
                $("#id_seat_matrix_table").prepend(
                    `<div class="card">
                    <div class="card-body">
                        <h2 class="card-title">${seat_matrix_data["college_name"]}</h2>
                        <h3 class="card-text">${seat_matrix_data["course_name"]}</h3>
                    </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">Total seats: <b>${seat_matrix_data["total_seats"]}</b></li>
                        <li class="list-group-item">Reserved for ${seat_matrix_data["reservation_category"]}: <b>${seat_matrix_data["reserved_seats"]}</b></li>
                        <li class="list-group-item">Total management seats: <b>60</b></li>
                    </ul>
                    <div class="card-footer text-muted">
                        To Know available Seats, Fees Structure & admission assistance kindly Call or Whatsapp to +919137386752
                    </div>
                </div>
                    `
                )
            }
        )
    }


}


