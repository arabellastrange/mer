"use strict";

var songURLMap = new Map();
var playlistURLMap = new Map();

function model() {
    this.init = function () {
        $.getJSON('playlists.json', generatePlaylists);
    };

    this.getPlaylistID = function (index) {
        return playlistURLMap.get(index);
    }
}

function onClientLoad() {
    console.log('loaded api');
    gapi.client.load('youtube', 'v3', onYouTubeApiLoad);
}

function onYouTubeApiLoad() {
    console.log('set key');
    gapi.client.setApiKey('AIzaSyBP9CxTGmOwsrV9DItzUnz9ZKLG6EVeImc');

}

function musicPlayerInit() {
    for (var i = 0; i < playlists.length; i++) {
        for (var n = 0; n < playlists[n].songs.length; n++) {
            var youtube_query = 'song+' + title + ' ' + artist;
            if(songURLMap.get(youtube_query)){
                song.set('url', songURLMap.get(youtube_query));
            } else{
                var youtube_url = searchYouTube(youtube_query);
                song.set('url', youtube_url);
                songURLMap.set(youtube_query, youtube_url);
            }
        }
    }

}

function createPlaylists(){
    for (var i = 0; i < playlists.length; i++) {
        // add songs to youtube playlist
        // put new playlist id as
        playlistURLMap.set(i, 'PLKLdE3o4nBsh7atlOsVxzEJ10Hj20dfuo');
    }
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