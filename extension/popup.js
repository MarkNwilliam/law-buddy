document.addEventListener("DOMContentLoaded", function () {
  const inputText = document.getElementById("inputText");
  const ask = document.getElementById('submit');
  const sendButton1 = document.getElementById("sendButton1");
  const sendButton2 = document.getElementById("sendButton2");

  let url;
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, async tabs => {
    url = tabs[0].url;
    console.log(url);
  }); 

  //Extension QA
  ask.addEventListener('click',() => {
    const text = inputText.value.trim();
    if (text === "") return;
    localStorage.setItem("url",url);
    localStorage.setItem("question",text);
    window.location.href="result.html";
  })

  //Law Buddy 
  sendButton1.addEventListener("click", async function () {
    window.open('https://law-buddy.streamlit.app/','_blank');
  });


  //Law Chatbot
  sendButton2.addEventListener("click", async function () {
      window.open('https://law-chatbot.streamlit.app','_blank');
  });
});
