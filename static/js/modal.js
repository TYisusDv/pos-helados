$(document).on('click', '.btn-modal', function() {
    var modalclass = $(this).attr("modalclass");
    var modal = document.querySelector(`.box.${modalclass}`);

    modal.classList.remove('d-none');
    modal.classList.add('d-flex');

    setTimeout(function() {
        modal.classList.add('active');
    }, 200);
});

$(document).on('click', '.modal__button--no', function() {
    var modalclass = $(this).attr("modalclass");
    var modal = document.querySelector(`.box.${modalclass}`);

    modal.classList.remove('active');

    setTimeout(function() {
        modal.classList.remove('d-flex');
        modal.classList.add('d-none');
    }, 500);
});