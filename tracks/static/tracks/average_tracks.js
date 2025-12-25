// we refrence: https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML for displaying the results in HTML
// we refrence: https://docs.djangoproject.com/en/6.0/topics/db/aggregation/ for calculating the averages


console.log("genre_averages.js loaded");

function getGenreAverages() {
    const genreInput = document.getElementById("genre_input");
    const resultDiv = document.getElementById("genre_result");

    const genre = genreInput?.value;
    // null check for the form
    if (!genre) {
        resultDiv.innerHTML =
            "<p style='color:red;'>Please enter a genre.</p>";
        return;
    }
    // send a GET request to the backend endpoint for genre averages
    fetch(`/api/genres/${genre}/averages/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Request failed: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // fill table with results in formatted HTML
        resultDiv.innerHTML = `
            <div class="stats-box">
                <h4>Average stats for genre: ${data.genre}</h4>

                <p><strong>Popularity:</strong> ${data.averages.popularity.toFixed(2)}</p>
                <p><strong>Acousticness:</strong> ${data.averages.acousticness.toFixed(2)}</p>
                <p><strong>Danceability:</strong> ${data.averages.danceability.toFixed(2)}</p>
                <p><strong>Energy:</strong> ${data.averages.energy.toFixed(2)}</p>
                <p><strong>Instrumentalness:</strong> ${data.averages.instrumentalness.toFixed(3)}</p>
                <p><strong>Duration:</strong> ${Math.round(data.averages.duration_ms)} ms</p>
            </div>
        `;
    });

}
