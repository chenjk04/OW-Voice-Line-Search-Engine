const main_searchbar = document.querySelector("#main_searchbar");
const main_form = main_searchbar.querySelector("#main_form");
const main_input = main_form.querySelector("#main_input");
const results_section = document.querySelector("#results");
const API_BASE_URL = "http://127.0.0.1:8000";

const clearResults = () => {
    results_section.replaceChildren();
}

const renderResults = (results) => {
    clearResults();

    if (!results || results.length === 0) {
        const emptyMessage = document.createElement("p");
        emptyMessage.className = "results_message";
        emptyMessage.textContent = "No matching voice lines found.";
        results_section.append(emptyMessage);
        return;
    }

    const heading = document.createElement("h2");
    heading.textContent = "Results";
    results_section.append(heading);

    const list = document.createElement("ul");
    list.className = "results_list";

    results.forEach((result) => {
        const item = document.createElement("li");
        item.className = "result_card";

        const hero = document.createElement("h3");
        hero.textContent = result.hero;

        const line = document.createElement("p");
        line.className = "result_line";
        line.textContent = result.line;

        const score = document.createElement("p");
        score.className = "result_score";
        score.textContent = `Match score: ${Number(result.score).toFixed(3)}`;

        item.append(hero, line, score);

        if (result.audio_url && result.ID) {
            const audio = document.createElement("audio");
            audio.controls = true;
            audio.src = `${API_BASE_URL}/api/audio/${encodeURIComponent(result.ID)}`;
            item.append(audio);
        }

        list.append(item);
    });

    results_section.append(list);
}

const sendSearchRequest = async (searchObj) => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/search`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(searchObj)
        });
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch(err) {
        console.error("Search request failed:", err);
        throw err;
    }
}

main_form.addEventListener("submit", async (event) => {
    event.preventDefault();
    event.stopPropagation();
    const queryVal = main_input.value.trim();
    const searchObj = {
        query: queryVal
    };
    const button = main_form.querySelector("button");
    button.disabled = true;
    results_section.innerHTML = "<p class=\"results_message\">Searching...</p>";

    try {
        const data = await sendSearchRequest(searchObj);
        renderResults(data.results);
    } catch (err) {
        results_section.innerHTML = "<p class=\"results_message\">Search failed. Check that the backend is running.</p>";
    } finally {
        button.disabled = false;
    }
})



