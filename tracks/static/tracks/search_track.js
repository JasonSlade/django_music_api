// search for a track given a specific thing, ie name or genre + return all tracks with that

console.log("search_track.js loaded");


function searchTrack() {
    const trackName = document.getElementById("track_name").value;
    const artistName = document.getElementById("artist_name").value;
    const genre = document.getElementById("genre").value;
    const popularity = document.getElementById("popularity").value;
    const danceability = document.getElementById("danceability").value;
    const energy = document.getElementById("energy").value;
    const duration = document.getElementById("duration").value;

    const params = new URLSearchParams();
    if (trackName) params.append("track_name", trackName);
    if (artistName) params.append("artist_name", artistName);
    if (genre) params.append("genre", genre);
    //if (popularity !== "") params.append("popularity", popularity);
    if (popularity) params.append("popularity", popularity);
    if (danceability) params.append("danceability", danceability);
    if (energy) params.append("energy", energy);
    if (duration) params.append("duration_ms", duration);

    // fetch to get tracks
    fetch(`/api/tracks/search/?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById("search_result");
            const tableBody = document.getElementById("results_body");

            // clear previous output
            resultDiv.innerHTML = `<h3>Found ${data.length} tracks</h3>`;
            tableBody.innerHTML = "";

            // limit results so browser doesn't freeze
            const limit = 1000;
            const rows = data.slice(0, limit);
            // display results
            rows.forEach(track => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${track.id}</td>
                    <td>${track.track_name}</td>
                    <td>${track.artist_name}</td>
                    <td>${track.genre}</td>
                    <td>${track.popularity}</td>
                    <td>${track.danceability}</td>
                    <td>${track.energy}</td>
                    <td>${track.duration_ms}</td>
                `;

                tableBody.appendChild(row);
            });
            // display how many of results
            if (data.length > limit) {
                resultDiv.innerHTML +=
                    `<p>Showing first ${limit} of ${data.length} results</p>`;
            }
        })
        .catch(error => {
            console.error("Search error:", error);
        });
}
