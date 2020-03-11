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

setcookie('visited', $isVisited, time() + (86400 * 7), "/"); //store for 7 days

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
    <script src="https://apis.google.com/js/client.js" type="text/javascript"></script>
    <script src="https://kit.fontawesome.com/8f0a84e548.js" crossorigin="anonymous"></script>
    <script src="https://www.youtube.com/iframe_api"></script>
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

<?php if (!$isVisited) { ?>
    <div id="user-agreement" class="modal fade" role="dialog" aria-hidden="true" aria-labelledby="user">
        <div id="user-profile-box" class="modal-dialog modal-dialog-centered modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="col-md-10 question-col">
                        <h5 id="user-header" class="modal-title">User Profile</h5>
                    </div>
                    <div class="col-md-2"></div>
                </div>
                <div class="profile-tab">
                    <div class="modal-body">
                        <p>This website collects your feedback and uses cookies to assign anonymized user IDs. By using
                            this site you understand and consent to the collection of your questionnaire answers for the
                            purpose of research at the University of Strathclyde. You understand that the information is
                            collected
                            for research purposes only and will not be used for any other purpose. You can begin a
                            feedback
                            session by clicking on the feedback button on every playlist and can skip any question with
                            which
                            you are uncomfortable and can further exist the session at any time. You are not obligated
                            to
                            complete this study, answer any particular question, or undertake any particular task which
                            you do not
                            wish to do. If you have completed a feedback session and wish to withdraw your data from the
                            study,
                            please contact <a href="chadha.degachi.2015@uni.strath.ac.uk">chadha.degachi.2015@uni.strath.ac.uk.</a>
                        </p>
                    </div>
                </div>

                <div class="profile-tab">
                    <div class="modal-body">
                        <form id="user-profile" method="post" action="user-profile.php" onsubmit="return profileSubmission()">
                            <div class="form-group">
                                <label id='selectMusicService' for="selectMusicServiceOptions" class="col-form-label">What
                                    services do you most often use to access music?</label>
                                <select class="form-control mdb-select md-form" id="selectMusicServiceOptions"
                                        name="music-purchase">
                                    <option>Youtube</option>
                                    <option>Streaming Subscription (Spotfiy, Google Music, Tidal,...)</option>
                                    <option>Purchased - Digital (iTunes, Amazon,...)</option>
                                    <option>Purchased - Hard Media (CD, Vinyl,...)</option>
                                    <option>Radio</option>
                                </select>
                                <label id="selectMusicCollection" for="selectMusicCollectionOptions"
                                       class="col-form-label">
                                    How do you most often group your music collection?</label>
                                <select class="form-control mdb-select md-form" id="selectMusicCollectionOptions"
                                        name="music-collection">
                                    <option>By Artist</option>
                                    <option>By Album</option>
                                    <option>By Genre</option>
                                    <option>By Era</option>
                                    <option>By Theme</option>
                                    <option>By Activity</option>
                                </select>
                            </div>
                            <input type="hidden" name="username" id="username" value="<?php echo $username; ?>">
                        </form>
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn btn-raised btn-lg btn-light" id="p-prevBtn" onclick="nextPrevP(-1)">
                        Back
                    </button>
                    <button type="button" class="btn btn-raised btn-lg" id="p-nextBtn" onclick="nextPrevP(1)">Continue
                    </button>
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
                    <div class="feedback-tab">
                        <div class="form-group">
                            <label class="col-form-label">What would you describe this playlist as?</label>
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="checkbox" id="inlineCheckboxHappy" value="true"
                                       name="happy-tag">
                                <label class="form-check-label" for="inlineCheckboxHappy">Happy, Cheerful,
                                    Upbeat</label>
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
                                <input class="form-check-input" type="checkbox" id="inlineCheckboxAngry"
                                       name="angry-tag"
                                       value="true">
                                <label class="form-check-label" for="inlineCheckboxAngry">Angry, Fiery,
                                    Passionate</label>
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
                            <label class="col-form-label">When would you listen to this playlist?</label>
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="checkbox" id="inlineCheckboxGym"
                                       name="event-op-gym"
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
                    </div>
                    <div class="feedback-tab">
                        <div class="form-group">
                            <label id='formTags' class="col-form-label">This playlist has been labelled as {} do you
                                agree?</label>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="agreeWithTags" id="agreeWithTags"
                                       value="yes" required>
                                <label class="form-check-label radio-label" for="agreeWithTags">Yes</label>
                                <input class="form-check-input" type="radio" name="agreeWithTags" id="disagreeWithTags"
                                       value="no" required>
                                <label class="form-check-label radio-label" for="disagreeWithTags">No</label>
                            </div>
                        </div>

                        <div class="form-group">
                            <label id="" class="col-form-label">How cohesive do you think this playlist is?</label>
                            <input type="range" name="cohesion" class="custom-range" min="1" max="5" step="1"
                                   list="playlist-tickmarks">
                            <datalist id='playlist-tickmarks'>
                                <option value='1' label='1'></option>
                                <option value='2'></option>
                                <option value='3' label='3'></option>
                                <option value='4'></option>
                                <option value='5' label='5'></option>
                            </datalist>
                        </div>
                    </div>
                    <div class="feedback-tab">
                        <div class='form-group'>
                            <label id='mlSliderQuestion' class='col-form-label'>How well do you think
                                this song fits the overall mood of the playlist?</label>
                            <div id="form-range">
                            </div>
                        </div>
                        <input type="hidden" name="username" id="username" value="<?php echo $username; ?>">
                    </div>
                </form>
            </div>

            <div class="modal-footer">
                <button type="button" class="btn btn-raised btn-lg btn-light" id="f-prevBtn" onclick="nextPrevF(-1)">Back
                </button>
                <button type="button" class="btn btn-raised btn-lg" id="f-nextBtn" onclick="nextPrevF(1)">Continue
                </button>
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
                        <p>Your unique username is: <span class="new-username"><?php echo $username ?></span></p>
                        <p>Please keep track of your username, if you wish to withdraw your submissions you can do so by
                            quoting this username and contacting the associated researchers.</p>
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

<div id="playlist-player" class="modal fade player" role="dialog">
    <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <div class="col-md-10"></div>
                <div class="col-md-2">
                    <button type="button" data-dismiss="modal" id="close-username" class="btn close"
                            aria-label="Close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <div class="modal-body" id="iframe-box"></div>
        </div>
    </div>
</div>

</body>
<footer>
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