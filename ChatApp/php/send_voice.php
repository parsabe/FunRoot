<?php
session_start();
include_once "config.php";

// must be POST with file + incoming_id
if (
  !isset($_SESSION['unique_id']) ||
  !isset($_POST['incoming_id']) ||
  !isset($_FILES['voice_data'])
) {
  echo json_encode(['success'=>false]);
  exit;
}

$out_id = mysqli_real_escape_string($conn, $_SESSION['unique_id']);
$in_id  = mysqli_real_escape_string($conn, $_POST['incoming_id']);

// save file
$ext = pathinfo($_FILES['voice_data']['name'], PATHINFO_EXTENSION);
$newName = time() . '_' . rand(1000,9999) . ".{$ext}";
$uploadDir = __DIR__ . "/voices/";
if (!is_dir($uploadDir)) mkdir($uploadDir, 0755, true);

if (move_uploaded_file($_FILES['voice_data']['tmp_name'], $uploadDir . $newName)) {
  // insert into DB (adjust table/columns to match yours)
  $msg = mysqli_real_escape_string($conn, "voices/{$newName}");
  $type = 'voice';
  $sql = "INSERT INTO messages (incoming_msg_id, outgoing_msg_id, message, msg_type)
          VALUES ('{$in_id}', '{$out_id}', '{$msg}', '{$type}')";
  if (mysqli_query($conn, $sql)) {
    echo json_encode(['success'=>true]);
    exit;
  }
}

// if we reach here, error
echo json_encode(['success'=>false]);
