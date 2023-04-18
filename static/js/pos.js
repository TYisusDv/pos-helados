var WL = window.location;
var WS = WL.search;
var WLPathname = WL.pathname;
var WLPathnameSplit = WLPathname.split('/');
let params = new URLSearchParams(WS);
var firstLoad = true;
var loader = `<div class="center animate__animated animate__bounceIn"><div class="center fs-30 mt-15 bg-white bor-primary circle w-50 h-50 p-20 fa-spin"><i class="fa-solid fa-ice-cream color-dark"></i></div></div>`;
var loader2 = `<div class="center animate__animated animate__bounceIn"><div class="center fs-25 mt-15 bg-white bor-primary circle w-30 h-30 p-20 mb-10 fa-spin"><i class="fa-solid fa-ice-cream color-dark"></i></div></div>`;
var CSRFToken = null;
var load = false;
let timeout;

//TABLE VARS
var table_url = null;
var table_search = "";
var page = 1;
var page_max = 1;

getCSRFToken();
setUrl(WLPathname);

function getCSRFToken() {
    $.ajax({
        url: `/api/v1/security/token/csrf`,
        type: 'post',
        async: false,
        dataType: "json",
        success: function(response) {
            if (response.success == false) {
                CSRFToken = null;
            } else {
                CSRFToken = response.token;
            }
        },
        error: function(xhr) {
            CSRFToken = null;
        }
    });

    return CSRFToken;
}

$("#menuButton").click(function() {
    if ($(".nav").attr("class") == "nav show") {
        $(".nav").attr("class", "nav hidde");
        $('.nav').animate({ "left": "-17rem" }, 400);
        $(".content").attr("class", "content full");
    } else {
        $(".nav").attr("class", "nav show");
        $('.nav').animate({ "left": "0px" }, 400);
        $(".content").attr("class", "content normal");
    }
});

$(".nav-top-user").click(function() {
    if ($(".nav-top-user-menu").css("display") == "none") {
        $(".nav-top-user-menu").css("display", "block");
    } else {
        $(".nav-top-user-menu").css("display", "none");
    }
});

$(".nav-li.level-1").click(function() {
    var navClass = $(this).attr("class");
    if (navClass.includes("active")) {
        $(this).removeClass("active");
        $("#" + $(this).attr("ul-id")).css("display", "none");
    } else {
        $(this).attr("class", $(this).attr("class") + " active");
        $("#" + $(this).attr("ul-id")).css("display", "block");
    }
});


function setUrl(url) {
    if (load == false) {
        load = true;

        history.pushState(null, `Enigma TM`, url);

        return getContent(url);
    }
}

function getContent(url) {
    $.ajax({
        url: `/api/v1/web/widget${url}`,
        type: 'post',
        async: false,
        dataType: "json",
        beforeSend: function(xhr, settings) {
            $("#content").html(loader);

            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", CSRFToken)
            }
        },
        success: function(response) {
            setTimeout(function() {
                load = false;

                if (response.success == false) {
                    return false;
                }

                $("#content").html(response.html);
                return true;
            }, 1200);
        },
        error: function(xhr) {
            setTimeout(function() {
                load = false;
                return false;
            }, 1200);
        }
    });
}

function setPagePrevious() {
    setn = page - 1;
    if (setn <= 0) {
        setn = 1
    }

    setPage(setn)
}

function setPageNext() {
    setn = page + 1;
    if (setn >= page_max) {
        setn = page_max
    }
    setPage(setn)
}

function setSearch(search) {
    table_search = search
    loadWidgetTable(table_url);
}

function setPage(num) {
    page = num;
    loadWidgetTable(table_url);
}

function loadWidgetTable() {
    $.ajax({
        url: `/api/v1/web/widget${table_url}`,
        type: 'post',
        data: { search: table_search, page: page },
        async: false,
        dataType: "json",
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", CSRFToken)
            }

            if (firstLoad == true) {
                $("#contentTable").html(loader2);
            }
        },
        success: function(response) {
            setTimeout(function() {
                if (response.success == false) {
                    return false;
                }

                $("#contentTable").html(response.html);
                return true;
            }, 1200);
        },
        error: function(xhr) {
            setTimeout(function() {
                return false;
            }, 1200);
        }
    });
}