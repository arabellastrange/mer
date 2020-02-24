"use strict"

function model() {
    this.init = function () {
        $.getJSON('playlists.json', generatePlaylists);

        window.onSpotifyWebPlaybackSDKReady = () => {
            const token = 'BQArf9j-GTYlZpCxjV2uE0AQT5mf3NpnSylJU8rO9iDWC8vcNrlvS5X4BnJs_9GIyuLw2qwxtDz6yZrVBZXlyTtjmiG0XRy5DaIvi01CYciLekES6-TugjAJTKiHAYSMX-flSpSwGnYpEzXN02OU5J0AUNtPsZ1478alack8ATk';
            const player = new Spotify.Player({
                name: 'Web Playback SDK Quick Start Player',
                getOAuthToken: cb => {
                    cb(token);
                }
            });

            // Error handling
            player.addListener('initialization_error', ({message}) => {
                console.error(message);
            });
            player.addListener('authentication_error', ({message}) => {
                console.error(message);
            });
            player.addListener('account_error', ({message}) => {
                console.error(message);
            });
            player.addListener('playback_error', ({message}) => {
                console.error(message);
            });

            // Playback status updates
            player.addListener('player_state_changed', state => {
                console.log(state);
            });

            // Ready
            player.addListener('ready', ({device_id}) => {
                console.log('Ready with Device ID', device_id);
            });

            // Not Ready
            player.addListener('not_ready', ({device_id}) => {
                console.log('Device ID has gone offline', device_id);
            });

            // Connect to the player!
            player.connect();
        };
    };

}