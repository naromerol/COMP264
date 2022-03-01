"use strict";

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
        langCell.class = "w3-center";
    });

}



async function uploadImage() {
    // encode input file as base64 string for upload
    let file = document.getElementById("file").files[0];
    let converter = new Promise(function(resolve, reject) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result
            .toString().replace(/^data:(.*,)?/, ''));
        reader.onerror = (error) => reject(error);
    });
    let encodedString = await converter;

    // clear file upload input field
    document.getElementById("file").value = "";

    // make server call to upload image
    // and return the server upload promise
    return fetch(serverUrl + "/images", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({filename: file.name, filebytes: encodedString})
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    })
}

function updateImage(image) {
    document.getElementById("view").style.display = "block";

    let imageElem = document.getElementById("image");
    imageElem.src = image["fileUrl"];
    imageElem.alt = image["fileId"];

    return image;
}

function translateImage(image) {
    // make server call to translate image
    // and return the server upload promise
    return fetch(serverUrl + "/images/" + image["fileId"] + "/translate-text", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({fromLang: "auto", toLang: "en"})
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new HttpError(response);
        }
    })
}

function annotateImage(translations) {
    let translationsElem = document.getElementById("translations");
    while (translationsElem.firstChild) {
        translationsElem.removeChild(translationsElem.firstChild);
    }
    translationsElem.clear
    for (let i = 0; i < translations.length; i++) {
        let translationElem = document.createElement("h6");
        translationElem.appendChild(document.createTextNode(
            translations[i]["text"] + " -> " + translations[i]["translation"]["translatedText"]
        ));
        translationsElem.appendChild(document.createElement("hr"));
        translationsElem.appendChild(translationElem);
    }
}

function uploadAndTranslate() {
    uploadImage()
        .then(image => updateImage(image))
        .then(image => translateImage(image))
        .then(translations => annotateImage(translations))
        .catch(error => {
            alert("Error: " + error);
        })
}

class HttpError extends Error {
    constructor(response) {
        super(`${response.status} for ${response.url}`);
        this.name = "HttpError";
        this.response = response;
    }
}
