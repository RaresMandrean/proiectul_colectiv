$(document).ready(function () {
    var users = document.getElementsByClassName('username');
    for (let i = 0; i < users.length; i++) {
        var buttons = document.getElementsByName(users[i].innerHTML);
        $(buttons[0]).click(function () {
            $.ajax({
                url: 'organiser-status/',
                data: {
                    'username': users[i].innerHTML,
                    'status': 'approved'
                },
                success: function () {
                    var btn_approve = document.getElementsByName(users[i].innerHTML)[0];
                    var btn_reject = document.getElementsByName(users[i].innerHTML)[1];
                    btn_approve.className = 'btn btn-success';
                    btn_approve.disabled = true;
                    btn_reject.className = 'btn btn-outline-danger';
                    btn_reject.disabled = false;
                }
            });

        });

        $(buttons[1]).click(function () {
            $.ajax({
                url: 'organiser-status/',
                data: {
                    'username': users[i].innerHTML,
                    'status': 'rejected'
                },
                success: function () {
                    var btn_reject = document.getElementsByName(users[i].innerHTML)[1];
                    var btn_approve = document.getElementsByName(users[i].innerHTML)[0];
                    btn_approve.className = 'btn btn-outline-success';
                    btn_approve.disabled = false;
                    btn_reject.className = 'btn btn-danger';
                    btn_reject.disabled = true;
                }
            });

        });
    }

});



