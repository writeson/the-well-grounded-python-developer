window.addEventListener('load', function (event) {
    let banner = document.querySelector("div.banner");
    window.addEventListener('click', function (event) {
        // is this the click event we're looking for?
        if (event.target.matches('#change-banner-color')) {
            let color = banner_colors[Math.floor(Math.random() * banner_colors.length)];
            banner.style.backgroundColor = color;
        }
    })
});
