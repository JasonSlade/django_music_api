// check file is loaded
console.log("delete_track.js loaded");

// to delete a track, we need track ID + use the DELETE HTTP method.
// we need to use a CSRF token in order to delete a track from the data base
/* 
For the CSRF token, we refrence: https://docs.djangoproject.com/en/6.0/howto/csrf/#using-csrf-protection-with-ajax
*/
function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}

function deleteTrack() {
    const trackId = document.getElementById("track_id").value;
    const resultDiv = document.getElementById("delete_result");

    if (!trackId) {
        resultDiv.innerHTML =
            "<p style='color:red;'>Please enter a Track ID.</p>";
        return;
    }

    fetch(`/api/tracks/${trackId}/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": getCSRFToken()   
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Delete failed");
        }
        //return response.json();
    })
    .then(data => {
        resultDiv.innerHTML =
            `<p style='color:green;'>Track ${trackId} deleted successfully.</p>`;
    })

}
