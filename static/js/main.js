const mobileButton =
    document.querySelector(".mobile-button");

const sidebar =
    document.querySelector(".sidebar");


if (mobileButton) {

    mobileButton.addEventListener("click", function() {

        sidebar.classList.toggle("show");

    });

}