<?php
    // sanitize input
    function clean_input($data){
        $data = trim($data);
        $data = stripcslashes($data);
        $data = htmlspecialchars($data);
        return $data;
    }

    //db settings
    $host = 'devweb2019.cis.strath.ac.uk';
    $user = 'wyb15135';
    $pass = 'vaiGh9Taecav';
    $dbname = 'wyb15135';
    $conn = new mysqli($host, $user, $pass, $dbname);

    // form vars
    $isOtherEvent = isset($_POST['event-op-other']) && ($_POST['event-op-other'] === 'true');
    $isOtherTag = isset($_POST['other-tag-op']) && ($_POST['other-tag-op'] === 'true');
    $isEventGym = isset($_POST['event-op-gym']) && ($_POST['event-op-gym'] === 'true');
    $isEventParty = isset($_POST['event-op-party']) && ($_POST['event-op-party'] === 'true');
    $isEventStudy = isset($_POST['event-op-study']) && ($_POST['event-op-study'] === 'true');
    $isEventRelax = isset($_POST['event-op-relax']) && ($_POST['event-op-relax'] === 'true');
    $isEventCommute = isset($_POST['event-op-commute']) && ($_POST['event-op-commute'] === 'true');
    $isTagHappy = isset($_POST['happy-tag']) && ($_POST['happy-tag'] === 'true');
    $isTagSad = isset($_POST['sad-tag']) && ($_POST['sad-tag'] === 'true');
    $isTagAngry = isset($_POST['angry-tag']) && ($_POST['angry-tag'] === 'true');
    $isTagRelax = isset($_POST['relax-tag']) && ($_POST['relax-tag'] === 'true');

    $userID = $_POST['username'];
    $playlistID = $_POST['playlist-id'];
    $cohesionRange = $_POST['cohesion'];

    $eventIn = NULL;
    $tagIn = NULL;

    $agreeTag = 0;

    $eventGym = 0;
    $eventParty = 0;
    $eventStudy = 0;
    $eventRelax = 0;
    $eventCommute = 0;
    $eventOther = 0;

    $tagHappy = 0;
    $tagSad = 0;
    $tagRelax = 0;
    $tagAngry = 0;
    $tagOther = 0;

    $fitnessArray = Array();

    if($_POST['agreeWithTags'] === 'yes'){
        $agreeTag = 1;
    }

    if($isEventGym){
        $eventGym = 1;
    }

    if($isEventParty){
        $eventParty = 1;
    }

    if($isEventRelax){
        $eventRelax = 1;
    }

    if($isEventStudy){
        $eventStudy = 1;
    }

    if($isEventCommute){
        $eventCommute = 1;
    }

    if ($isOtherEvent) {
        $eventOther = 1;
        $eventIn = clean_input(strip_tags($_POST['other-event-in']));
    }

    if ($isOtherTag) {
        $tagOther = 1;
        $tagIn = clean_input(strip_tags($_POST["other-tag-in"]));
    }

    if($isTagHappy){
        $tagHappy = 1;
    }

    if($isTagAngry){
        $tagAngry = 1;
    }

    if($isTagSad){
        $tagSad = 1;
    }

    if($isTagRelax){
        $tagRelax = 1;
    }

    foreach($_POST as $key => $value){
        if(strpos($key, 'range')){
            array_push($fitnessArray, $value);
        }
    }

    // Connect to MySQL
    if ($conn->connect_error) {
        die("Connection Failed!");
    }

    // Query

    $sql = "INSERT INTO `musicEvalFeedback` (`response_id`, `user_id`, `playlist_id`, `event_gym`, `event_party`, `event_study`, `event_relax`, `event_commute`, `event_other`, `event_input`, `tag_happy`, `tag_sad`, `tag_relax`, `tag_angry`, `tag_other`, `tag_input`, `ml_tag_eval`, `playlist_cohesion`, `song_0_fitness`, `song_1_fitness`, `song_2_fitness`, `song_3_fitness`, `song_4_fitness`, `song_5_fitness`, `song_6_fitness`, `song_7_fitness`) VALUES (NULL, '$userID', '$playlistID', '$eventGym', '$eventParty', '$eventStudy', '$eventRelax', '$eventCommute', '$eventOther', '$eventIn', '$tagHappy', '$tagSad', '$tagRelax', '$tagAngry', '$tagOther', '$tagIn', '$agreeTag', '$cohesionRange', '$fitnessArray[0]', '$fitnessArray[1]', '$fitnessArray[2]', '$fitnessArray[3]', '$fitnessArray[4]', '$fitnessArray[5]', '$fitnessArray[6]', '$fitnessArray[7]')";

    $result = $conn->query($sql);

    // Handle Result
    if(!$result){
        die("Query failed!");
    }

    //Disconnect
    $conn->close();

