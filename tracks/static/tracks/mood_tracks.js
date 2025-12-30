// mood classifier

console.log("moods.js loaded");

// loads mood data from server + renders to page
function loadMood(mood) {
    const heading = document.getElementById("mood_heading");
    const list = document.getElementById("mood_results");

    heading.textContent = `Loading ${mood} tracks...`;
    list.innerHTML = "";
    // gets the mood 
    fetch(`/api/moods/${mood}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Request failed");
            }
            return response.json();
        })
        // takes JSON returned from server + renders list of tracks 
        .then(data => {
            heading.textContent =
                `${data.mood.toUpperCase()} tracks (${data.count})`;

            if (data.tracks.length === 0) {
                list.innerHTML = "<li>No tracks found.</li>";
                return;
            }
            // creates list items for each track
            data.tracks.forEach(track => {
                const item = document.createElement("li");
                item.textContent =
                    `${track.track_name} – ${track.artist_name} (${track.genre})`;
                list.appendChild(item);
            });
        })
        .catch(error => {
            console.error(error);
            heading.textContent = "Error loading tracks.";
        });
}
