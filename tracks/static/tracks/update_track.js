let currentTrackId = null;

/* 
For the CSRF token, we refrence: https://docs.djangoproject.com/en/6.0/howto/csrf/#using-csrf-protection-with-ajax
*/
function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}

// first step in this page is to load the track, so that the user can see the current content of the track
function loadTrack() {
    const trackId = document.getElementById("trackIdInput").value;

    if (!trackId) {
        alert("Enter a track ID");
        return;
    }
    // simple fetch to get the track data
    fetch(`/api/track/${trackId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Track not found");
            }
            return response.json();
        })
        .then(data => {
            currentTrackId = trackId;

            document.getElementById("genre").value = data.genre ?? "";
            document.getElementById("artist_name").value = data.artist_name ?? "";
            document.getElementById("track_name").value = data.track_name ?? "";
            document.getElementById("popularity").value = data.popularity ?? 0;
            document.getElementById("acousticness").value = data.acousticness ?? 0;
            document.getElementById("danceability").value = data.danceability ?? 0;
            document.getElementById("duration_ms").value = data.duration_ms ?? 0;
            document.getElementById("energy").value = data.energy ?? 0;
            document.getElementById("instrumentalness").value = data.instrumentalness ?? 0;
        })
        .catch(err => alert(err.message));
}

// second part is to update the track
function updateTrack() {
    if (!currentTrackId) {
        alert("Load a track first");
        return;
    }
    // new data we will load into the track
    const payload = {
        genre: document.getElementById("genre").value,
        artist_name: document.getElementById("artist_name").value,
        track_name: document.getElementById("track_name").value,

        popularity: document.getElementById("popularity").value || 0,
        acousticness: document.getElementById("acousticness").value || 0,
        danceability: document.getElementById("danceability").value || 0,
        duration_ms: document.getElementById("duration_ms").value || 0,
        energy: document.getElementById("energy").value || 0,
        instrumentalness: document.getElementById("instrumentalness").value || 0,
    };
    // post the new data to the database
    fetch(`/api/track/${currentTrackId}/update/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(payload),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Update failed");
            }
            return response.json();
        })
        .then(data => {
            //alert(`Track ${data.id} updated successfully`);
        })
        .catch(err => alert(err.message));
}
