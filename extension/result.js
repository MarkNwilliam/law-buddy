// Wait for the document to be fully loaded
const readRequestDiv = document.getElementById("readRequest");
let ans;

document.addEventListener("DOMContentLoaded", function () {
    // Select the loading SVG with the id "here"
    var loadingSvg = document.getElementById("here");

    async function load(){
        const resp1 = await fetch("https://hostingwebgpt-1-k3041194.deta.app/upload", {
            method: "POST",
            body: JSON.stringify({
              "website": localStorage.getItem("url"),
            }),
            headers: {
              "Content-type": "application/json; charset=UTF-8"
            }
        })
        .then((response) => response.json())
        .then((json) => console.log(json));

        //query
        const resp2 = await fetch("https://hostingwebgpt-1-k3041194.deta.app/query", {
            method: "POST",
            body: JSON.stringify({
              "query": localStorage.getItem("question"),
            }),
            headers: {
              "Content-type": "application/json; charset=UTF-8"
            }
        })
        const resp = await resp2.json();
        ans = resp.result;
        
        loadingSvg.remove();
        readRequestDiv.innerHTML = ans;
    }
    load(); 
});