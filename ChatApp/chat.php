<?php
session_start();
include_once "php/config.php";
if (!isset($_SESSION['unique_id'])) {
  header("location: login.php");
}
?>
<?php include_once "header.php"; ?>

<body>
  <div class="wrapper">
    <section class="chat-area">
      <header>
        <?php
        $user_id = mysqli_real_escape_string($conn, $_GET['user_id']);
        $sql = mysqli_query($conn, "SELECT * FROM users WHERE unique_id = {$user_id}");
        if (mysqli_num_rows($sql) > 0) {
          $row = mysqli_fetch_assoc($sql);
        } else {
          header("location: users.php");
        }
        ?>
        <a href="users.php" class="back-icon"><i class="fas fa-arrow-left"></i></a>
        <div class="details">
          <span>
            <?php
            $fname_short = substr($row['fname'], 0, 2);
            $namer = $fname_short . '_' . $row['lname'] . '@' . $row['username'];
            echo $namer;
            ?>
          </span>
          <p><?php echo $row['status']; ?></p>
        </div>

      </header>
      <div class="chat-box">

      </div>
      <form action="#" class="typing-area" id="chat-form">
  <input type="text" class="incoming_id" name="incoming_id"
         value="<?php echo $user_id; ?>" hidden>

  <!-- text input -->
  <input type="text" name="message" class="input-field"
         placeholder="Type a message here..." autocomplete="off">

  <!-- hidden file input for voice blobs -->
  <input type="file" name="voice_data" id="voiceDataInput" style="display:none">

  <!-- audio‐level meter (hidden until recording) -->
  <div id="voiceMeterWrap" style="display:none; margin:0 5px; vertical-align:middle;">
    <div id="voiceMeter" style="width:100px; height:5px; background:#eee;">
      <div id="voiceLevel" style="width:0%; height:100%; background:#76c7c0;"></div>
    </div>
  </div>

  <!-- send text -->
  <button type="submit" class="send-text-btn">
    <i class="fab fa-telegram-plane"></i>
  </button>

  <!-- record & send voice -->
  <button type="button" class="voice-btn" id="voice-btn">
    <i class="fas fa-microphone"></i>
  </button>
</form>




    </section>
  </div>

  <script src="javascript/chat.js"></script>

</body>

</html>