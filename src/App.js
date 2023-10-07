import { useState, useEffect } from "react";

function App() {
  const [imageUrl, setImageUrl] = useState();
  const [storyText, setStoryText] = useState();
  const [words, setWords] = useState({first: '', second: '', third: ''});
  const [messages, setMessages] = useState();
  const iteration = 0;

 useEffect(()=>{
    // initial run
    // fetch('/api/test').then(res => res.json()).then(data => {console.log(data.text)});
    fetch('/api/initialize').then(res => res.json()).then(data => {setImageUrl(data.image_url); setMessages(data.messages); setStoryText(data.story_text); console.log("API response recvd")})
  }, []);

  function handleSubmit (e) {
    e.preventDefault();
    setImageUrl('src/loadingImage.png')
    setStoryText("LOADING NEXT PART " + storyText)
    fetch('/api/continue', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'messages': messages, 'word_1': words.first, 'word_2': words.second, 'word_3': words.third})
    }).then(res => res.json()).then(data => {setImageUrl(data.image_url); setMessages(data.messages); setStoryText(data.story_text); console.log("API response recvd")});
    // continue story, giving words.first, words.second, words.third
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setWords((prevWords) => ({ ...prevWords, [name]: value }));
  };

  return (
    <div className="App">

      <div className="content">
        <img className='image-container' src={imageUrl}></img>
        <p style={{position: 'absolute', top: 0, left: '512px', height: '512px', overflowY: 'scroll'}}>{storyText}</p>
      </div>


      <div className="input-form">
        <form style={{position: 'absolute', top: '540px'}} onSubmit={handleSubmit}>

          <input type="text" id="first" name="first" value={words.first} onChange={handleChange}/>

          <input type="text" id="second" name="second" value={words.second} onChange={handleChange}/>

          <input type="text" id="third" name="third" value={words.third} onChange={handleChange}/>

          <button type="submit">Continue Story</button>

        </form>
      </div>


    </div>
  );
}

export default App;
