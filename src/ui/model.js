"use strict";

var songURLMap = new Map();

function model() {
    this.init = function () {
        $.getJSON('playlists.json', generatePlaylists);
    };
}

function get_spotify_url(query) {
    var accessToken = 'bcc543d6f5564761ac2548ded2bdd20d';
    var headers = new Headers();
    var options = {
        method: 'GET',
        headers: {
            Authorization: 'Bearer' + accessToken
        }
    };

    fetch(query, options).then(
        response => console.log(response)
    );
}

function onClientLoad() {
    console.log('loaded api');
    gapi.client.load('youtube', 'v3', onYouTubeApiLoad);
}

function onYouTubeApiLoad() {
    console.log('set key');
    gapi.client.setApiKey('AIzaSyBP9CxTGmOwsrV9DItzUnz9ZKLG6EVeImc');
    $.getJSON('playlists.json', musicPlayerInit);
}

function musicPlayerInit(playlists) {
    console.log('amplitude set up');
    var songs = [];

    Amplitude.init({
        "songs": [],
        "playlist": {},
        "volume": 35,
        "default_album_art": "/img/blue-grid.png",
        "default_playlist_art": "/img/blue-grid.png"
    });

    for (var m = 0; m < playlists.length; m++) {
        var playlist_key = 'playlist' + i;
        var play_title = "{title: 'untitled playlist #" + i + "'}";
        Amplitude.addPlaylist(playlist_key, play_title, []);
        Amplitude.bindNewElements();
    }

    for (var i = 0; i < playlists.length; i++) {
        for (var n = 0; n < playlists[n].songs.length; n++) {
            var playlist_key = 'playlist' + i;
            var artist = playlists[i].songs[n].artist;
            var song_title = playlists[i].songs[n].title;
            var url = 'music/bensound-uklele.mp3';
            var song_key = 'song-' + i + '-' + n;

            // var spotify_query = 'https://api.spotify.com/v1/search?q=name:' + title.replace(' ', '%20') + '%20artist:' + artist.replace(' ', '%20') + '&type=track';
            // var youtube_query = 'song+' + title + ' ' + artist;
            // if(songURLMap.get(youtube_query)){
            //     song.set('url', songURLMap.get(youtube_query));
            // } else{
            //     var youtube_url = searchYouTube(youtube_query);
            //     song.set('url', youtube_url);
            //     songURLMap.set(youtube_query, youtube_url);
            // }

            var song = "{'name': '" + song_title + "', 'artist': '" + artist + "', 'url': '" + url + "', 'made_up_key': '" + song_key + "'}";
            Amplitude.addSongToPlaylist(song, playlist_key);
            Amplitude.bindNewElements();
        }
    }

    Amplitude.bindNewElements();
    console.log(Amplitude.getConfig());


}

function searchYouTube(query) {
    // Use the JavaScript client library to create a search.list() API call.
    var request = gapi.client.youtube.search.list({
        part: 'snippet',
        q: encodeURIComponent(query).replace(/%20/g, "+"),
        order: 'viewCount'
    });
    // Send the request to the API server, call the onSearchResponse function when the data is returned
    request.execute(onSearchResponse);
}

function onSearchResponse(response) {
    var responseString = JSON.stringify(response, '', 2);
    var results = response.results;
    $.each(results.items, function (index, item) {
        console.log(item);
    });
    console.log(responseString)
}

function feedbackSubmission() {
    $.ajax({
        type: 'POST',
        url: 'form.php',
        data: $('#user-feedback').serialize(),
        success: function (response) {
            console.log('Yay: ' + response)
        }
    });
    // should move to view
    $('#feedback').modal('hide');

    if ($('#new-username').length > 0) {
        $('#new-username').modal('show');
    }

    return false;
}