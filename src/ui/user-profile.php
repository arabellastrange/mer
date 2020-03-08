<?php
    $host = 'devweb2019.cis.strath.ac.uk';
    $user = 'wyb15135';
    $pass = 'vaiGh9Taecav';
    $dbname = 'wyb15135';
    $conn = new mysqli($host, $user, $pass, $dbname);

    $userID = $_POST['username'];
    $musicCollection = $_POST['music-collection'];
    $musicPurchase = $_POST['music-purchase'];

    // Connect to MySQL
    if ($conn->connect_error) {
        die("Connection Failed!");
    }

    // Query
    $sql = "INSERT INTO `musicUserProfile` (`user_id`, `music_service`, `music_collection`) VALUES ('$userID', '$musicPurchase', '$musicCollection');";

    $result = $conn->query($sql);

    // Handle Result
    if(!$result){
        die("Query failed!");
    }

    //Disconnect
    $conn->close();

