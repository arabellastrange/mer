"use strict";

var songURLMap = new Map();
var collatedPlaylist = [];
var allModels = ['playlists_deep_class.json', "playlists_forest_class.json", "playlists_lforest_class.json",
    'playlists_svm_class.json', "playlists_lsvm_class.json"];


function model() {
    this.init = function () {
        $.getJSON('playlists.json', generatePlaylists);

        // for (var i = 0; i < allModels.length; i++){
        //     $.getJSON(allModels[i], function (playlists) {
        //         createPlaylist(playlists)
        //     });
        // }
    };

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


function feedbackSubmission() {
    $.ajax({
        type: 'POST',
        url: 'form.php',
        data: $('#user-feedback').serializeArray(),
        success: function (response) {
            console.log('sucess')
        }
    });

    $('#feedback').modal('hide');

    window.location.reload(false);

    return false;
}

function createPlaylist(playlists) {
    console.log('creating');
    var possible_playlists = [];
    var rand_playlists = [];

    for (var i = 0; i < playlists.length; i++) {
        var playlist = playlists[i];
        if(playlist.random === true){
            rand_playlists.push(playlist)
        } else {
            var song_tags = [];
            playlist.songs.forEach(s => song_tags.push(s.tags));

            if(song_tags.length > 0){
                possible_playlists.push(playlist)
            }
        }
    }

    var rand_int_p_1 = Math.floor(Math.random() * possible_playlists.length);
    collatedPlaylist.push(possible_playlists[rand_int_p_1]);

    var rand_int_p_2 = Math.floor(Math.random() * possible_playlists.length);
    if (rand_int_p_1 !== rand_int_p_2){
        collatedPlaylist.push(possible_playlists[rand_int_p_2]);
    } else{
        rand_int_p_2 = Math.floor(Math.random() * possible_playlists.length);
        collatedPlaylist.push(possible_playlists[rand_int_p_2]);
    }

    var rand_int_r =  Math.floor(Math.random() * rand_playlists.length);
    collatedPlaylist.push(rand_playlists[rand_int_r]);

    console.log(collatedPlaylist);

}


function readPlaylists() {
    generatePlaylists(collatedPlaylist);
}

function profileSubmission() {
    $.ajax({
        type: 'POST',
        url: 'user-profile.php',
        data: $('#user-profile').serializeArray(),
        success: function (response) {
            console.log('success')
        }
    });

    $('#user-agreement').modal('hide');

    if ($('#new-username').length > 0) {
        $('#new-username').modal('show');
    }

    return false;
}