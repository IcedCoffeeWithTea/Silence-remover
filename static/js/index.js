const audio = document.getElementById("audio")
const audio_label = document.getElementById("audio-label")

addEventListener("change", (event) => {
    if (event.target == audio) {
        audio_label.textContent = audio.files[0].name
    }
})

