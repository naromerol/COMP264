"use strict";

// NESTOR ROMERO - 301133331
// COMP264 MIDTERM

//API Endpoint base url
const serverUrl = "http://127.0.0.1:8000";

async function translateReviews() {
    
    // page processing pipeline
    translate().then( response => display(response));

}

function translate() {
    return fetch(serverUrl + "/reviews", {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        //body: JSON.stringify({fromLang: "auto", toLang: "en"})
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    })
}

function display(content) {

    // Unpack content
    let count = content['review_count']
    let reviews = content['reviews']

    //DOM references
    let review_tablebody = document.getElementById("reviews").getElementsByTagName("tbody")[0];
    let rev_count = document.getElementById("rev_count");
    rev_count.appendChild(document.createTextNode(count));

    // Create review table
    reviews.forEach(function(review){
        let newRow = review_tablebody.insertRow();
        let lineCell = newRow.insertCell();
        lineCell.appendChild(document.createTextNode(review['line']));
        lineCell.style.width = "45%";
        let translationCell = newRow.insertCell();
        translationCell.appendChild(document.createTextNode(review['translation']));
        translationCell.style.width = "45%";
        let langCell = newRow.insertCell();
        langCell.appendChild(document.createTextNode(review['lang']));
        langCell.className = "w3-center";
    });

}
