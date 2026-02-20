const main_searchbar = document.querySelector("#main_searchbar");
const main_form = main_searchbar.querySelector("#main_form");
const main_input = main_form.querySelector("#main_input");
console.log(main_searchbar);
console.log(main_form);

const sendSearchRequest = async (searchObj) => {
    try {
        const response = await fetch("https://httpbin.org/post", { // /api/search
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
        //
        console.log(data);
        return data;
    } catch(err) {
        console.error("Search request failed:", err);
    }
}

main_form.addEventListener("submit", async (event) => {
    event.preventDefault();
    event.stopPropagation();
    const queryVal = main_input.value.trim();
    console.log(queryVal.length);
    const searchObj = {
        query: queryVal
    };
    const button = main_form.querySelector("button");
    button.disabled = true;

    try {
        await sendSearchRequest(searchObj);
    } finally {
        button.disabled = false;
    }
})



