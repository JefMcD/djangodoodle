

function get_unsplash_pic(){
    let app_id = 767659
    let access_key = "SXBZ0U_g0ocuUcH3ZJzDGUAJu7cAmz8EkGDhTCtt37I"
    let secret_key = "lRioI8fGKrhHeFIyFTMZoSLIfIMFKza4K1ywFZTQGKE"

    // Public Auth https://api.unsplash.com/photos/?client_id=YOUR_ACCESS_KEY
    let api_url = "https://api.unsplash.com/photos/random?client_id=SXBZ0U_g0ocuUcH3ZJzDGUAJu7cAmz8EkGDhTCtt37I"

    // Make a GET request
    fetch(api_url, {
        method: "GET",
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        console.log("Description:", data.description); // Access top-level 'description' field
        console.log("Regular URL:", data.urls.regular); // Access 'regular' nested under 'urls'
        console.log(data)

        random_pic = `
        <img src="{}
        `

    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function add_unsplash_api_get_button(){
    const api_get_btn = document.getElementById('unsplash-api-get-btn')
    api_get_btn.addEventListener('click', get_unsplash_pic)
    return
}

document.addEventListener('DOMContentLoaded', function() {
    add_unsplash_api_get_button();
})