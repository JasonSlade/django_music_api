console.log("create_track.js loaded");


/* 
For the CSRF token, we refrence: https://docs.djangoproject.com/en/6.0/howto/csrf/#using-csrf-protection-with-ajax
*/
function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}


function submitTrack() {
   var newTrack = {
    genre: document.getElementById("genre").value,
    artist_name: document.getElementById("artist_name").value,
    track_name: document.getElementById("track_name").value,
    popularity: parseInt(document.getElementById("popularity").value),
    acousticness: parseFloat(document.getElementById("acousticness").value),
    danceability: parseFloat(document.getElementById("danceability").value),
    duration_ms: parseInt(document.getElementById("duration_ms").value),
    energy: parseFloat(document.getElementById("energy").value),
    instrumentalness: parseFloat(document.getElementById("instrumentalness").value)
};


    fetch('/api/tracks/create/', {
    method: "POST",
    credentials: "same-origin",
    headers: {
        "X-CSRFToken": getCSRFToken(),
        "Content-Type": "application/json"
    },
    body: JSON.stringify(newTrack)
})
.then(response => {
    if (!response.ok) {
        throw new Error("Network response was not ok");
    }
    return response.json();
})
.then(data => {
    console.log("Track created:", data);
    document.getElementById("create_result").innerHTML =
        `<p style="color: green;">Track created with ID ${data.id}</p>`;
})
.catch(error => {
    console.error("Error creating track:", error);
    document.getElementById("create_result").innerHTML =
        `<p style="color: red;">Error creating track.</p>`;
});

}



document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM loaded");

    document
        .getElementById("submitBtn")
        .addEventListener("click", submitTrack);
});
