<?php
session_start();
if (!isset($_SESSION['unique_id'])) {
    header("Location: ../login.php");
    exit;
}
include_once "config.php";

// cast to int
$outgoing_id = (int) $_SESSION['unique_id'];
$incoming_id = (int) $_POST['incoming_id'];

$output = "";

// pull all messages between these two users
$sql = "
  SELECT
    msg_id,
    msg,
    msg_type,
    outgoing_msg_id
  FROM messages
  WHERE
      (outgoing_msg_id = {$outgoing_id} AND incoming_msg_id = {$incoming_id})
   OR (outgoing_msg_id = {$incoming_id} AND incoming_msg_id = {$outgoing_id})
  ORDER BY msg_id ASC
";
$query = mysqli_query($conn, $sql);

if ($query && mysqli_num_rows($query) > 0) {
    while ($row = mysqli_fetch_assoc($query)) {
        $msgId      = (int)$row['msg_id'];
        $isOutgoing = ((int)$row['outgoing_msg_id'] === $outgoing_id);
        $cls        = $isOutgoing ? 'outgoing' : 'incoming';

        // rawMsg holds "voices/xxxxx.webm" for voice, or text
        $rawMsg = htmlspecialchars($row['msg'], ENT_QUOTES);
        $type   = $row['msg_type'];

        $output .= "<div class=\"chat {$cls}\" data-msg-id=\"{$msgId}\">"
                 .  "<div class=\"details\">";

        if ($type === 'voice') {
            // PLAY BUTTON + inline WAVEFORM bars
            $url = "php/{$rawMsg}";
            $output .= "
              <div class=\"voice-message\" style=\"display:flex; align-items:center;\">
                <audio class=\"voice-audio\" preload=\"none\" src=\"{$url}\"></audio>
                <button class=\"toggle-play-btn\" style=\"border:none;background:none;font-size:1.2em;cursor:pointer;margin-right:8px;\">
                <i class='fas fa-play'></i></button>
                <div class=\"voice-waveform\" style=\"display:flex;gap:3px;\">
                  <div class=\"bar\" style=\"width:3px;height:12px;background:#ccc;animation:wave 1s infinite;animation-delay:0s;\"></div>
                  <div class=\"bar\" style=\"width:3px;height:16px;background:#ccc;animation:wave 1s infinite;animation-delay:0.1s;\"></div>
                  <div class=\"bar\" style=\"width:3px;height:10px;background:#ccc;animation:wave 1s infinite;animation-delay:0.2s;\"></div>
                  <div class=\"bar\" style=\"width:3px;height:14px;background:#ccc;animation:wave 1s infinite;animation-delay:0.3s;\"></div>
                  <div class=\"bar\" style=\"width:3px;height:8px;background:#ccc;animation:wave 1s infinite;animation-delay:0.4s;\"></div>
                  <div class=\"bar\" style=\"width:3px;height:18px;background:#ccc;animation:wave 1s infinite;animation-delay:0.5s;\"></div>
                </div>
              </div>
              <style>
                @keyframes wave {
                  0%,100% { transform: scaleY(1); }
                  50%     { transform: scaleY(0.5); }
                }
              </style>
            ";
        } else {
            // TEXT
            $output .= "<p>" . nl2br($rawMsg) . "</p>";
        }

        $output .= "</div></div>";
    }
} else {
    $output .= '
      <div class="text">
        No messages yet — say hello!
      </div>
    ';
}

echo $output;
