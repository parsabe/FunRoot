<?php
session_start();
include_once "config.php";

$outgoing_id = $_SESSION['unique_id'];
$searchTerm  = mysqli_real_escape_string($conn, $_POST['searchTerm']);

$sql = "
  SELECT *
  FROM users
  WHERE unique_id != {$outgoing_id}
    AND (
      fname    LIKE '%{$searchTerm}%'
      OR lname    LIKE '%{$searchTerm}%'
      OR username LIKE '%{$searchTerm}%'
    )
";
$query  = mysqli_query($conn, $sql);
$output = "";

if(mysqli_num_rows($query) > 0){
    while($row = mysqli_fetch_assoc($query)){
        // hide yourself
        $hid_me = ($row['unique_id'] === $outgoing_id) ? "hide" : "";

        // online/offline
        $offline = ($row['status'] === "Offline now") ? "offline" : "";

        // display name
        $fname_short = substr($row['fname'], 0, 2);
        $namer       = "{$fname_short}_{$row['lname']}@{$row['username']}";

        // initials avatar
        $initials = strtoupper(
            substr($row['fname'], 0, 1) .
            substr($row['lname'], 0, 1)
        );  

        // build snippet
        $output .= '
        <a href="chat.php?user_id='.$row['unique_id'].'" class="'.$hid_me.'">
          <div class="content">
            <div class="details">
              <span>'.$namer.'</span>
            </div>
          </div>
          <div class="status-dot '.$offline.'"><i class="fas fa-circle"></i></div>
        </a>';
    }
} else {
    $output = 'No user found related to your search term';
}

echo $output;
?>
