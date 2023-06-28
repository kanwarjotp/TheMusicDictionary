// record song function
async function getMedia(constraints) {
  let stream = null;

  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: false,
      audio: true,
    });
    first_track = stream.getAudioTracks()[0];
    // console.log(first_track)

    //   create a media recorder
    recorder = new MediaRecorder(stream);
    recorder.addEventListener("dataavailable", handleRecData);

    recorder.start();
    // alert(recorder.state)
    updtButton(1);

    setTimeout(function () {
      recorder.stop();
      first_track.stop();
      // alert("recording stopped")
      updtButton(2);
    }, 10000);
  } catch (err) {
    /* handle the error */
    alert("mic denied!");
    alert(err);
  }
}

//   using AJAX to send the BLOB data to the backend.
function handleRecData(event) {
  // console.log(event.data)
  const rec_sample = new Blob([event.data], { type: "audio/wav" });
  const sample_url = URL.createObjectURL(rec_sample);
  // console.log(sample_url)
  const rec_audio = new Audio(sample_url);

  // sending the data to server
  const send_req = new XMLHttpRequest();
  var save_form = new FormData();
  save_form.append("sample_data", rec_sample, "rec_sample");
  send_req.open("POST", "/process_sample", true);
  send_req.send(save_form);

  // request song identification
  askForPrediction();
}

async function askForPrediction() {
  // grabbing URL from the HTML document
  const pred_url = document.getElementById("prediction-link").innerHTML;

  const start_time = Date.now();

  fetch(pred_url)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      const pred_div = document.getElementById("prediction");
      const time_div = document.getElementById("timeTaken");

      const end_time = Date.now();
      const time_taken = ((end_time - start_time) / 1000).toFixed(1);

      pred_div.innerHTML = data["ans"];
      time_div.innerHTML = "Song identfied in ".concat(time_taken).concat("s");

      updtButton(3);

      // updating the button to record a new song
      setTimeout(function () {
        updtButton(0);
      }, 5000);
    });
}

function updtButton(value) {
  const bttn = document.getElementById("rec-bttn");
  if (value == 0) {
    bttn.disabled = false;
    bttn.innerHTML = "click to record";
    bttn.style = "background-color: #0d6efd";
  } else if (value == 1) {
    bttn.disabled = true;
    bttn.innerHTML = "recording";
    bttn.style = " background-color: red;";
  } else if (value == 2) {
    bttn.disabled = true;
    bttn.innerHTML = "working";
    bttn.style = " background-color: black;";
  } else if (value == 3) {
    bttn.disabled = true;
    bttn.innerHTML = "song found!";
    bttn.style = " background-color: green;";
  }
}
