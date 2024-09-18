// import { useState } from 'react'
import './App.css'

function App() {
  return (
    <>
      <div>
        {/* <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="true" />
        <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet" /> */}
        <body>
          <div className="title-area">
            <img src="https://storage.googleapis.com/transcribler_icons/Logo1_35x103.png" alt="Transcribler Logo" className="logo" />
            <div className="roboto-bold , h1-box">
              Transcribler
            </div>
            <div className="tab">
              <button className="tablinks active" id="defaultOpen">
                Video Information
              </button>
            </div>

            <div id="Summary" className="tabcontent">
              <div>
                Topics
              </div>
              <br />
              <div className="output-box">
                <p id="topics">
                </p>
              </div>
              <div>
                Summary <br/>
              </div>
              <br />
              <div className="output-box">
                <p id="output">
                </p>
              </div>
              <div>
                Age Rating
              </div>
              <br />
              <div className="output-box">
                <p id="age">
                </p>
              </div>
              <div>
                Fake News
              </div>
              <br />
              <div className="output-box">
                <p id="fakenews">
                </p>
              </div>
              <div>
                Toxicity
              </div>
              <br />
              <div className="output-box">
                <p id="toxicity">
                </p>
              </div>
              <div>
                Sentiment Analysis
              </div>
              <br />
              <div className="output-box">
                <p id="sentiment">
                </p>
              </div>
            </div>
            <script src="Popup.js">
            </script>
          </div>
        </body>
      </div>
    </>
  )
}

export default App
