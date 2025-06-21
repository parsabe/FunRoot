<?php
session_start();
if (!isset($_SESSION['unique_id'])) {
    header("Location: ../login.php");
    exit;
}

include_once "config.php";

$outgoing_id = $_SESSION['unique_id'];
$incoming_id = mysqli_real_escape_string($conn, $_POST['incoming_id']);
$msg_type   = 'text';
$message    = '';


if (
    isset($_FILES['voice_data']) &&
    $_FILES['voice_data']['error'] === UPLOAD_ERR_OK &&
    strpos($_FILES['voice_data']['type'], 'audio/') === 0
) {
    // build a unique filename
    $ext       = pathinfo($_FILES['voice_data']['name'], PATHINFO_EXTENSION) ?: 'webm';
    $newName   = time() . '_' . rand(1000, 9999) . '.' . $ext;
    $uploadDir = __DIR__ . '/voices/';

    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0755, true);
    }

    // move it into place
    if (move_uploaded_file($_FILES['voice_data']['tmp_name'], $uploadDir . $newName)) {
        $message  = 'voices/' . $newName;
        $msg_type = 'voice';
    } else {
        http_response_code(500);
        echo 'UPLOAD_FAILED';
        exit;
    }

// 2) Otherwise, treat it as a text message
} elseif (isset($_POST['message'])) {
    $text = trim($_POST['message']);
    if ($text === '') {
        // nothing to insert
        exit;
    }
    $message = mysqli_real_escape_string($conn, $text);
    $msg_type = 'text';

} else {
    // neither text nor audio => nothing to do
    exit;
}

// sanitize again just in case
$message = mysqli_real_escape_string($conn, $message);

// 3) Insert into DB
$sql = "
    INSERT INTO messages 
      (incoming_msg_id, outgoing_msg_id, msg, msg_type)
    VALUES 
      ({$incoming_id}, {$outgoing_id}, '{$message}', '{$msg_type}')
";
if (mysqli_query($conn, $sql)) {
    // success
    echo 'OK';
} else {
    http_response_code(500);
    echo 'DB_ERROR';
}
