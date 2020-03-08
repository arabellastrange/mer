"use strict";

var childElement, appendChildElement, player;
var all_playlists = new Map();
var submitProfileButton = document.getElementById('submit-profile'),
    playlistGallery = document.getElementById('playlist-gallery'),
    feedback = document.getElementById('feedback'),
    formRange = document.getElementById('form-range'),
    formTags = document.getElementById('formTags'),
    playBannerButton = document.getElementById('playBannerButton'),
    pauseBannerButton = document.getElementById('pauseBannerButton'),
    playlistBanner = document.getElementById('playlist-controls'),
    currentSong = document.getElementById('current-song'),
    otherEventButton = document.getElementById('inlineCheckboxOtherEvent'),
    otherTagButton = document.getElementById('inlineCheckboxOtherTag');
var done = false;

var currentPTab = 0;
var currentFTab = 0;

function view() {
    showPTab(currentPTab);
    showFTab(currentFTab);

    this.setUserAgreement = function () {
        console.log('modal loaded');
        if ($('#user-agreement').length > 0) {
            $('#user-agreement').modal({
                backdrop: false
            });
        }
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
                var scale_id = '-song-' + play_no + '-' + i;
                songs = songs + "<div><label class='song-label'>" + playlist.songs[i].artist + ' - ' + playlist.songs[i].title + "</label><input type='range' name='song-range" + scale_id + "' class='custom-range' min='1' max='5' id='" + scale_id + "' step='1' list='song-tickmarks'><datalist id='song-tickmarks'><option value='1' label='1'></option><option value='2'></option><option value='3' label='3'></option><option value='4'></option><option value='5' label='5'></option></datalist></div><div><input type='hidden' name='playlist-id' value='" + play_no + "'></div>";
                tags = tags.concat(playlist.songs[i].tags);
            }
            formRange.innerHTML = songs;

            let unique_tags = tags.filter((item, i, ar) => ar.indexOf(item) === i);
            formTags.innerText = 'This playlist has been labelled as ' + unique_tags + ' do you agree?';

        });

    }

}

function setPlayFunc(buttonID) {
    var playlistIndex = buttonID.substring(buttonID.indexOf('-'), buttonID.length);
    var playlistYoutubeID = getPlaylistYoutubeId(playlistIndex);
    player = new YT.Player('video-placeholder', {
        width: '100%',
        height: '100%',
        listType: 'playlist',
        list: playlistYoutubeID,
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });

    playlistBanner.style.display = 'block';
    currentSong.innerHTML = all_playlists.get(playlistIndex).songs[player.getPlaylistIndex()];

}

function onPlayerReady(event) {
    event.target.playVideo();
}

function onPlayerStateChange(event) {
    if (event.data === YT.PlayerState.PLAYING && !done) {
        setTimeout(stopVideo, 6000);
        done = true;
    }
}

function stopVideo() {
    player.stopVideo();
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
        appendChildElement.innerHTML = '<div id="playlist-' + i + '" class = "col-md-4"><div class="card playlist"><div class="card-body"><h3 class="card-title playlist-title">Playlist ' + i + '</h3><div class="card-text song-list"' + html_play + '</div></div><div class="row btn-row"><button id="play-' + i + '"class="btn" type="button" onClick="setPlayFunc(this.id)"><i class="fas fa-play"></i></button><button type="button" class="btn" id="feedbackButton" data-toggle="modal" data-target="#feedback"  data-whatever= ' + i + '><i class="fas fa-clipboard"></i></button></div></div></div>';

    }
}

function showFTab(n){
    var m = document.getElementsByClassName("feedback-tab");
    if (m.length > 0) {
        m[n].style.display = "block";
        if (n === 0) {
            document.getElementById("f-prevBtn").style.display = "none";
        } else {
            document.getElementById("f-prevBtn").style.display = "inline";
        }
        if (n === (m.length - 1)) {
            document.getElementById("f-nextBtn").innerHTML = "Submit";
        } else {
            document.getElementById("f-nextBtn").innerHTML = "Continue";
        }
    }
}

function showPTab(n) {
    // This function will display the specified tab of the form ...
    var x = document.getElementsByClassName("profile-tab");

    if (x.length > 0) {
        x[n].style.display = "block";
        // ... and fix the Previous/Next buttons:
        if (n === 0) {
            document.getElementById("p-prevBtn").style.display = "none";
        } else {
            document.getElementById("p-prevBtn").style.display = "inline";
        }
        if (n === (x.length - 1)) {
            document.getElementById("p-nextBtn").innerHTML = "Submit";
        } else {
            document.getElementById("p-nextBtn").innerHTML = "Continue";
        }
    }
}

function nextPrevF(n) {
    var m = document.getElementsByClassName('feedback-tab');
    console.log(m);

    if(m.length > 0) {
        console.log('switching tabs');
        m[currentFTab].style.display = "none";
        currentFTab = currentFTab + n;
        if (currentFTab >= m.length) {
            feedbackSubmission();
            return false;
        }
    }

    showFTab(currentFTab);

}

function nextPrevP(n) {
    // This function will figure out which tab to display
    var x = document.getElementsByClassName("profile-tab");

    // Hide the current tab:
    if(x.length > 0){
        x[currentPTab].style.display = "none";
        currentPTab = currentPTab + n;
        // if you have reached the end of the form... :
        if (currentPTab >= x.length) {
            profileSubmission();
            return false;
        }
    }

    showPTab(currentPTab);
}

