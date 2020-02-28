"use strict"

var childElement, appendChildElement;
var all_playlists = new Map();
var agreeButton = document.getElementById('agreeButton'),
    submitProfileButton = document.getElementById('submit-profile'),
    playlistGallery = document.getElementById('playlist-gallery'),
    playButton = document.getElementById('playButton'),
    feedback = document.getElementById('feedback'),
    formRange = document.getElementById('form-range'),
    formTags = document.getElementById('formTags'),
    playBannerButton = document.getElementById('playBannerButton'),
    pauseBannerButton = document.getElementById('pauseBannerButton'),
    otherEventButton = document.getElementById('inlineCheckboxOtherEvent'),
    otherTagButton = document.getElementById('inlineCheckboxOtherTag');

function view() {
    this.setSubmitProfileButtonFunc = function (){
        submitProfileButton.addEventListener('click', function (e) {
            //
        });
    };

    this.setUserAgreement = function () {
        console.log('modal loaded');
        $('#user-agreement').modal({
            backdrop: false
        });
    };

    this.setOtherEventFunc = function () {
        otherEventButton.addEventListener('change', function (e) {
            console.log('setting listener on other event');
            $("input[id='otherEventInput']").prop('disabled', this.value === 0);
        })
    };
    this.setOtherTagFunc = function () {
        otherTagButton.addEventListener('change', function (e) {
            console.log('setting listener on other tag');
            $("input[id='otherTagInput']").prop('disabled', this.value === 0);
        })
    };

    this.generateSongListForm = function () {
        $('#feedback').on('show.bs.modal', function (e) {
            var button = $(e.relatedTarget); // Button that triggered the modal
            var play_no = button.data('whatever'); // Extract info from data-* attributes
            var playlist = all_playlists.get(play_no);
            var songs = "";
            var tags = [];

            console.log(playlist);
            for (var i = 0; i < playlist.songs.length; i++) {
                var scale_id = "songScale" + play_no + i;
                songs = songs + "<div><label class='song-label'>" + playlist.songs[i].artist + ' - ' + playlist.songs[i].title + "</label><input type='range' class='custom-range' min='1' max='5' id='" + scale_id + "' step='1' list='tickmarks'><datalist id='tickmarks'><option value='1' label='1'></option><option value='2'></option><option value='3' label='3'></option><option value='4'></option><option value='5' label='5'></option></datalist></div>";
                tags = tags.concat(playlist.songs[i].tags);
            }
            formRange.innerHTML = songs;

            let unique_tags = tags.filter((item, i, ar) => ar.indexOf(item) === i);
            formTags.innerText = 'Would you describe this playlist as: ' + unique_tags;

        });

    }

}

function sendEvent(sel, step) {
    $(sel).trigger('next.m.' +step)
}

function setPlayFunc() {
    // for every play button on each playlist add listener
    for (var i = 0; i < playButton.length; i++) {
        playButton.item(i).addEventListener("click",
            function (e) {
                // do smth
            });
    }
}

function generatePlaylists(playlists) {
    for (var i = 0; i < playlists.length; i++) {
        all_playlists.set(i, playlists[i]);
        childElement = document.createElement('div');
        appendChildElement = playlistGallery.appendChild(childElement);
        var html_play = "<ul class='song-list'>";
        for (var n = 0; n < playlists[i].songs.length; n++) {
            var song_format = "<li>" + playlists[i].songs[n].artist + ' - ' + playlists[i].songs[n].title + "</li>";
            html_play = html_play + song_format;
        }
        html_play = html_play + "</ul>";
        appendChildElement.innerHTML = '<div id="playlist" class = "col-md-4 playlist card">' + html_play + '<div class="row btn-row"><button id="playButton" class="btn" type="button">play</button><button type="button" class="btn" id="feedbackButton" data-toggle="modal" data-target="#feedback"  data-whatever= ' + i + '> feedback </button></div></div>';

    }
}