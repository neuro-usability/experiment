
var global = {};
var filename = 'file';
// SDK Needs to create video and canvas nodes in the DOM in order to function
// Here we are adding those nodes a predefined div.
var divRoot = $("#affdex_elements")[0];
var width = 320;
var height = 240;
var faceMode = affdex.FaceDetectorMode.LARGE_FACES;
//Construct a CameraDetector and specify the image width / height and face detector mode.
var detector = new affdex.CameraDetector(divRoot, width, height, faceMode);
var emojiList = {
  "joy": "😂",
  "unanmused": "😒",
  "heart-eyes": "😍",
  "relaxed": "😌",
  "kissing-heart": "😘",
  "blush": "😊",
  "pensive":"😔",
  "weary": "😩",
  "sob": "😭",
  "smirk": "😏",
  "grin": "😁",
  "flushed": "😳",
  "wink": "😉",
  "rage": "😡",
  "scream": "😱",
  "kiss": "💋",
  "stuckout-tongue-eyes-closed": "😝",
  "tongue": "👅",
  "mouth": "👄",
  "stuckout-tongue": "😛",
  "relieved": "😌",
  "expressionless": "😑",
  "yum": "😋",
  "stuckout-tongue-winking-eye": "😜",
  "disappointed": "😞",
  "smile": "😄",
  "sleeping": "😴",
  "neutral-face": "😐",
  "sweat-smile": "😅",
  "smiley": "😃",
  "angry": "😠",
  "grimacing": "😬",
  "laughing": "😆",
  "kissing-closed-eyes": "😚",
  "grinning": "😀"
}
window.onload = function() {
  jQuery.each(emojiList, function(emojiKey) {
    var slide = document.createElement("div");
    var emoji = document.createElement("div");
    slide.className = "carousel-cell";
    emoji.className = "big-emoji";
    emoji.innerHTML = emojiList[emojiKey];
    slide.appendChild(emoji);
    document.getElementById("carousel").appendChild(slide);
    console.log(emojiList[emojiKey]);
  });
  var flkty = new Flickity('.carousel', {
    pageDots: false
  });
};


//Enable detection of all Expressions, Emotions and Emojis classifiers.
detector.detectAllEmotions();
detector.detectAllExpressions();
detector.detectAllEmojis();
detector.detectAllAppearance();

//Add a callback to notify when the detector is initialized and ready for runing.
detector.addEventListener("onInitializeSuccess", function() {

  log('#logs', "The detector reports initialized");
  //Display canvas instead of video feed because we want to draw the feature points on it
  $("#face_video_canvas").css("display", "block");
  $("#face_video").css("display", "none");
});

function log(node_name, msg) {
  $(node_name).append("<span>" + msg + "</span><br />")
}

var record = false;
var recording = false;
$('#record').on('mousedown', function() {
  record = true;
});
$('#record').on('mouseup', function() {
  record = false;
  recording = false;
});
//function executes when Start button is pushed.
function onStart() {
  if (detector && !detector.isRunning) {
    $("#logs").html("");
    detector.start();
  }
  log('#logs', "Clicked the start button");
}

//function executes when the Stop button is pushed.
function onStop() {
  log('#logs', "Clicked the stop button");
  if (detector && detector.isRunning) {
    detector.removeEventListener();
    detector.stop();
  }
};

//function executes when the Reset button is pushed.
function onReset() {
  log('#logs', "Clicked the reset button");
  if (detector && detector.isRunning) {
    detector.reset();

    $('#results').html("");
  }
};

//Add a callback to notify when camera access is allowed
detector.addEventListener("onWebcamConnectSuccess", function() {
  log('#logs', "Webcam access allowed");
});

//Add a callback to notify when camera access is denied
detector.addEventListener("onWebcamConnectFailure", function() {
  log('#logs', "webcam denied");
  console.log("Webcam access denied");
});

//Add a callback to notify when detector is stopped
detector.addEventListener("onStopSuccess", function() {
  log('#logs', "The detector reports stopped");
  $("#results").html("");
});

//Add a callback to receive the results from processing an image.
//The faces object contains the list of the faces detected in an image.
//Faces object contains probabilities for all the different expressions, emotions and appearance metrics
detector.addEventListener("onImageResultsSuccess", function(faces, image, timestamp) {
  $('#results').html("");
  log('#results', "Timestamp: " + timestamp.toFixed(2));
  log('#results', "Number of faces found: " + faces.length);
  if (faces.length > 0) {
    log('#results', "Appearance: " + JSON.stringify(faces[0].appearance));
    log('#results', "Emotions: " + JSON.stringify(faces[0].emotions, function(key, val) {
      return val.toFixed ? Number(val.toFixed(0)) : val;
    }));
    log('#results', "Expressions: " + JSON.stringify(faces[0].expressions, function(key, val) {
      return val.toFixed ? Number(val.toFixed(0)) : val;
    }));
    log('#results', "Emoji: " + faces[0].emojis.dominantEmoji);
    drawFeaturePoints(image, faces[0].featurePoints);
  }
});

//Draw the detected facial feature points on the image
function drawFeaturePoints(img, featurePoints) {
  var contxt = $('#face_video_canvas')[0].getContext('2d');

  var hRatio = contxt.canvas.width / img.width;
  var vRatio = contxt.canvas.height / img.height;
  var ratio = Math.min(hRatio, vRatio);

  contxt.strokeStyle = "#FFFFFF";
  for (var id in featurePoints) {
    contxt.beginPath();
    contxt.arc(featurePoints[id].x,
      featurePoints[id].y, 2, 0, 2 * Math.PI);
    contxt.stroke();

  }
}

console.save = function(data, filename){

    if(!data) {
        console.error('Console.save: No data')
        return;
    }

    if(!filename) filename = 'console.json'

    if(typeof data === "object"){
        data = JSON.stringify(data, undefined, 4)
    }

    var blob = new Blob([data], {type: 'text/json'}),
        e    = document.createEvent('MouseEvents'),
        a    = document.createElement('a')

    a.download = filename
    a.href = window.URL.createObjectURL(blob)
    a.dataset.downloadurl =  ['text/json', a.download, a.href].join(':')
    e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
    a.dispatchEvent(e)
 }
