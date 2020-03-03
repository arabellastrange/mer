<?php
$username = 'none';
$newUserName = false;
$isVisited = false;

$host = 'devweb2019.cis.strath.ac.uk';
$user = 'wyb15135';
$pass = 'vaiGh9Taecav';
$dbname = 'wyb15135';
$conn = new mysqli($host, $user, $pass, $dbname);

if (isset($_COOKIE['username'])) {
    $username = $_COOKIE['username'];
    $newUserName = false;
    $isVisited = true;
} else {
    $new_name = 'user' . mt_rand(0, 10000);
    // Connect to MySQL
    if ($conn->connect_error) {
        die("Connection Failed!");
    }
    // Query and Handle Result
    if (check_user_name_already_exists($new_name, $conn)) {
        $new_name = 'user' . mt_rand(0, 10000);
    }
    //Disconnect
    $conn->close();

    $newUserName = true;
    $username = $new_name;
    // write username to cookie
    setcookie('username', $username, time() + (86400 * 7), "/"); //store for 7 days
}

setcookie('visited', $isVisited,  time() + (86400 * 7), "/"); //store for 7 days

function check_user_name_already_exists($new_name, $conn)
{
    $select = $conn->query("select * from `musicEvalFeedback` where user_id='$new_name'");
    if ($select) {
        return true;
    } else {
        return false;
    }
} ?>

<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/html">
<head>
    <meta charset="UTF-8">
    <meta name="mobile-web-app-capable" content="yes"/>
    <meta name="apple-mobile-web-app-capable" content="yes"/>

    <!-- spotify web sdk -->
    <script src="https://code.jquery.com/jquery-3.4.1.js"
            integrity="sha256-WpOohJOqMqqyKL9FccASB9O0KwACQJpFTUBLTYOVvVU=" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/popper.js@1.12.6/dist/umd/popper.js"
            integrity="sha384-fA23ZRQ3G/J53mElWqVJEGJzU0sTs+SvzG8fXVWP+kJQ1lwFAOkcUOysnlKJC33U"
            crossorigin="anonymous"></script>
    <script src="https://unpkg.com/bootstrap-material-design@4.1.1/dist/js/bootstrap-material-design.js"
            integrity="sha384-CauSuKpEqAFajSpkdjv3z9t8E7RlpJ1UP0lKM/+NdtSarroVKu069AlsRPKkFBz9"
            crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/amplitudejs@v5.0.3/dist/amplitude.js"></script>
    <script src="https://apis.google.com/js/client.js" type="text/javascript"></script>
    <script src="https://kit.fontawesome.com/8f0a84e548.js" crossorigin="anonymous"></script>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
          integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet"
          href="https://unpkg.com/bootstrap-material-design@4.1.1/dist/css/bootstrap-material-design.min.css"
          integrity="sha384-wXznGJNEXNG1NFsbm0ugrLFMQPWswR3lds2VeinahP8N0zJw9VWSopbjv2x7WCvX" crossorigin="anonymous">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons">
    <link rel="stylesheet" type="text/css" href="view.css">

    <link rel="icon" size="192x192" href="img/color-casette.png">
    <link rel="apple-touch-icon" href="img/color-casette.png">
    <link rel="shourtcut icon" href="img/color-casette.png" type="image/x-icon">

    <title>ML Playlist Generator</title>
</head>
<body>
<!--<script src="https://sdk.scdn.co/spotify-player.js"></script>-->
<!--<script>-->
<!--    window.onSpotifyWebPlaybackSDKReady = () => {-->
<!--        const token = 'BQCpu3XuDABpN33fOXtbAxEXO2Fg2cZFgfQ5ow4xCeaN-ivtG1qNS1o2DLXuiZoTLmoNctBpcy7-hlyfHlQuDP_b-2k6-FoPjWDN2Ac0pU88hHdVsyhOZ98ei301I5pxc-ftOZ2C4yn5PJfTvmuTCkrJOtshNxcUMyQODxMZIHc';-->
<!--        const player = new Spotify.Player({-->
<!--            name: 'Web Playback SDK Quick Start Player',-->
<!--            getOAuthToken: cb => { cb(token); }-->
<!--        });-->
<!---->
<!--        // Error handling-->
<!--        player.addListener('initialization_error', ({ message }) => { console.error(message); });-->
<!--        player.addListener('authentication_error', ({ message }) => { console.error(message); });-->
<!--        player.addListener('account_error', ({ message }) => { console.error(message); });-->
<!--        player.addListener('playback_error', ({ message }) => { console.error(message); });-->
<!---->
<!--        // Playback status updates-->
<!--        player.addListener('player_state_changed', state => { console.log(state); });-->
<!---->
<!--        // Ready-->
<!--        player.addListener('ready', ({ device_id }) => {-->
<!--            console.log('Ready with Device ID', device_id);-->
<!--        });-->
<!---->
<!--        // Not Ready-->
<!--        player.addListener('not_ready', ({ device_id }) => {-->
<!--            console.log('Device ID has gone offline', device_id);-->
<!--        });-->
<!---->
<!--        // Connect to the player!-->
<!--        player.connect();-->
<!--    };-->
<!--</script>-->

<div class="row">
    <div class="logo-text col-md-12" id='logo-text'>
        <h1>MER-ML</h1>
    </div>
</div>
<div class="row">
    <div id="main" class="col-md-12">
        <div id="playlist-gallery"></div>
    </div>
</div>

<?php if(!$isVisited) { ?>
    <div id="user-agreement" class="modal fade" role="dialog" aria-hidden="true" aria-labelledby="user">
        <div id="user-profile-box" class="modal-dialog modal-dialog-centered modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="col-md-10 question-col">
                        <h5 id="user-header" class="modal-title">User Profile</h5>
                    </div>
                    <div class="col-md-2"></div>
                </div>
                <div class="modal-body">
                    <p>This website collects your feedback and uses cookies to assign anonymized user IDs. By using this
                        site you understand and consent to the collection of your questionnaire answers for the purpose of
                        research at the University of Strathclyde. You understand that the information is collected for
                        research purposes only and will not be used for any other purpose. You can begin a feedback session
                        by clicking on the feedback button on every playlist and can skip any question with which you are
                        uncomfortable and can further exist the session at any time. You are not obligated to complete this
                        study, answer any particular question, or undertake any particular task which you do not wish to do.
                        If you have completed a feedback session and wish to withdraw your data from the study, please
                        contact <a href="chadha.degachi.2015@uni.strath.ac.uk">chadha.degachi.2015@uni.strath.ac.uk.</a></p>
                </div>
                <!-- <div class="modal-body step step-2" data-step="2">
                    <form>
                        <div class="form-group">
                            <label id='selectMusicService' for="selectMusicServiceOptions" class="col-form-label">What
                                services do you most often use to access music?</label>
                            <select class="form-control" id="selectMusicServiceOptions">
                                <option>Youtube</option>
                                <option>Streaming Subscription (Spotfiy, Google Music, Tidal,...)</option>
                                <option>Purchased - Digital (iTunes, Amazon,...)</option>
                                <option>Purchased - Hard Media (CD, Vinyl,...)</option>
                                <option>Radio</option>
                            </select>
                            <label id="selectMusicCollection" for="selectMusicCollectionOptions" class="col-form-label">
                                How do you most often group your music collection?</label>
                            <select class="form-control" id="selectMusicCollectionOptions">
                                <option>By Artist</option>
                                <option>By Album</option>
                                <option>By Genre</option>
                                <option>By Era</option>
                                <option>By Theme</option>
                                <option>By Activity</option>
                            </select>
                        </div>
                    </form>
                </div> -->
                <div class="modal-footer">
                    <button type="button" class="btn btn-raised btn-lg" id="agreeButton"
                            data-dismiss="modal">Continue
                    </button>
                    <!-- <button type="button" class="btn btn-primary" id="submit-profile">Submit
                    </button> -->
                </div>
            </div>
        </div>
    </div>
<?php } ?>

<div id='feedback' class="modal fade" tabindex="-1" role="dialog" aria-hidden="true" aria-labelledby="question">
    <div id="feedback-box" class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <div class="col-md-10 question-col">
                    <h5 id='question-header' class="modal-title">Feedback Questionnaire</h5>
                </div>
                <div class="col-md-2">
                    <button type="button" data-dismiss="modal" id='close-feedback' class="btn close" aria-label="Close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <div class="modal-body">
                <form id='user-feedback' action="form.php" method="post" onsubmit="return feedbackSubmission()">
                    <div class="form-group">
                        <label class="col-form-label">When would you listen to this playlist?</label>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckboxGym" name="event-op-gym"
                                   value="true">
                            <label class="form-check-label" for="inlineCheckboxGym">Gym</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckboxParty"
                                   name="event-op-party" value="true">
                            <label class="form-check-label" for="inlineCheckboxParty">Party</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckboxStudying"
                                   name="event-op-study" value="true">
                            <label class="form-check-label" for="inlineCheckboxStudying">Studying</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckboxRelaxing"
                                   name="event-op-relax" value="true">
                            <label class="form-check-label" for="inlineCheckboxRelaxing">Relaxing</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckboxCommute"
                                   name="event-op-commute" value="true">
                            <label class="form-check-label" for="inlineCheckboxCommute">Commute</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckboxOtherEvent"
                                   value="true" name="event-op-other">
                            <label class="form-check-label" for="inlineCheckboxOtherEvent">Other</label>
                        </div>
                        <label class="col-form-label" for="otherEventInput">Other: </label>
                        <input id='otherEventInput' name="other-event-in" class="form-control" type="text" disabled>
                    </div>
                    <div class="form-group">
                        <label class="col-form-label">What would you describe this playlist as?</label>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckboxHappy" value="true"
                                   name="happy-tag">
                            <label class="form-check-label" for="inlineCheckboxHappy">Happy, Cheerful, Upbeat</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckboxSad" value="true"
                                   name="sad-tag">
                            <label class="form-check-label" for="inlineCheckboxSad">Sad, Melancholy, Gloomy</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckboxRelax" value="true"
                                   name="relax-tag">
                            <label class="form-check-label" for="inlineCheckboxRelax">Slow, Relaxed, Chill</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckboxAngry" name="angry-tag"
                                   value="true">
                            <label class="form-check-label" for="inlineCheckboxAngry">Angry, Fiery, Passionate</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckboxOtherTag"
                                   value="true" name="other-tag-op">
                            <label class="form-check-label" for="inlineCheckboxOtherTag">Other</label>
                        </div>
                        <label class="col-form-label" for="otherTagInput">Other: </label>
                        <input id='otherTagInput' name="other-tag-in" class="form-control" type="text" disabled>
                    </div>
                    <div class="form-group">
                        <label id='formTags' class="col-form-label">Would you describe this playlist as: {}?</label>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="agreeWithTags" id="agreeWithTags"
                                   value="yes" required>
                            <label class="form-check-label radio-label" for="agreeWithTags">Yes</label>
                            <input class="form-check-input" type="radio" name="agreeWithTags" id="disagreeWithTags"
                                   value="no" required>
                            <label class="form-check-label radio-label" for="disagreeWithTags">No</label>
                        </div>
                    </div>
                    <div class='form-group'><label id='mlSliderQuestion' class='col-form-label'>How well do you think
                            this song fits the overall mood of the playlist?</label>
                        <div id="form-range">
                        </div>
                    </div>
                    <input type="hidden" name="username" id="username"
                           value="<?php echo $username; ?>">
                    <input type="submit" class="btn btn-raised btn-lg"/>
                </form>
            </div>
            <div class="modal-footer">
                <!-- etc -->
            </div>
        </div>
    </div>
</div>

<?php if ($newUserName) { ?>
    <div id="new-username" class="modal fade" tabindex="-1" role="dialog" aria-hidden="true"
         aria-labelledby="new-username">
        <div id="new-username-box" class="modal-dialog modal-dialog-centered modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="col-md-10">
                        <h5 class="modal-title">Thank you for your submission!</h5>
                    </div>
                    <div class="col-md-2">
                        <button type="button" data-dismiss="modal" id="close-username" class="btn close"
                                aria-label="Close">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                <div class="modal-body">
                    <div class="col-md-12">
                        <p>Your unique username is:<span class="new-username"><?php echo $username ?></span></p>
                        <p>Please keep track of your username, if you wish to withdraw your submissions you can do so by
                            quoting
                            this username and contacting the associated researchers.</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-raised btn-lg" data-dismiss="modal" aria-label="Close">OK
                    </button>
                </div>
            </div>
        </div>
    </div>
<?php } ?>


</body>
<footer>
    <div class="row playlist-controls">
        <div id="currentlyPlaying" class="col-md-12">
            <div class="col-md-3 player-controls">
                <i id="song-icon" class="fas fa-microphone"></i>
                <i class="fas fa-backward control-icon" id="rewind-button"></i>
                <i id="play-button" class="fas fa-play control-icon"></i>
                <i id="pause-button" class="fas fa-pause control-icon"></i>
                <i id="skip-button" class="fas fa-forward control-icon"></i>
            </div>
            <div class="col-md-6"></div>
            <div class="col-md-3"></div>
        </div>
    </div>

    <div class="row footer">
        <div class="col-md-1"></div>
        <div class="col-md-10">
            <p> This web page is associated with the final year project of Chadha Degachi at the University of
                Strathclyde. This project aims to improve automatic playlist generation by the use of machine learning
                for mood recognition in music. You will be asked to provide feedback on your perceived emotion of these
                playlist samples and what context you feel they are best suited for. Supervisor: Dr. Marc Roper: <a
                        href="marc.roper@strath.ac.uk">marc.roper@strath.ac.uk</a>. CIS Ethic Committee: <a
                        href="ethics@cis.strath.ac.uk">ethics@cis.strath.ac.uk</a></p>
        </div>
        <div class="col-md-1"></div>
    </div>
    <script src="model.js"></script>
    <script src="view.js"></script>
    <script src="controller.js"></script>
</footer>
</html>