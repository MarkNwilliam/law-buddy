// Wait for the document to be fully loaded
const readRequestDiv = document.getElementById("readRequest");
let ans;

document.addEventListener("DOMContentLoaded", function () {

    // let send_data = require('./popup.cjs');
    // console.log(send_data);


    // Select the loading SVG with the id "here"
    var loadingSvg = document.getElementById("here");

    // Remove the SVG after 3 seconds
    // setTimeout(function () {
    //     if (loadingSvg && loadingSvg.parentNode) {
    //         loadingSvg.parentNode.removeChild(loadingSvg);
    //     }

    //     // Select the readRequest div
    //     var readRequestDiv = document.getElementById("readRequest");

    //     // Add textual content within the readRequest div
    //     if (readRequestDiv) {
    //     readRequestDiv.innerHTML = localStorage.getItem("url")+" "+localStorage.getItem("question");
    //     }
    //     // window.onload = alert(localStorage.getItem("inputValue"));

    // }, 2000);


    async function load(){
        // send url req
        const resp1 = await fetch("https://website_gpt-1-m6489679.deta.app/upload", {
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
    const resp2 = await fetch("https://website_gpt-1-m6489679.deta.app/query", {
    method: "POST",
    body: JSON.stringify({
      "query": localStorage.getItem("question"),
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  })
    // .then((response) => response.json())
    // .then((json) => console.log(json.result));   
    // const ans = await resp2.result;
    // // readRequestDiv.innerHTML = ans;

    const resp = await resp2.json();
    console.log(resp)
    ans = resp.result;
    // ans = response.result;
    // console.log(ans);

    console.log("from backend: "+ans);
        loadingSvg.remove();
        readRequestDiv.innerHTML = ans;
           
    }
    load();
    
});
