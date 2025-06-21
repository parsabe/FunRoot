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
    <section class="users">
      <header>
        <div class="content">
          <?php
          $sql = mysqli_query($conn, "SELECT * FROM users WHERE unique_id = {$_SESSION['unique_id']}");
          if (mysqli_num_rows($sql) > 0) {
            $row = mysqli_fetch_assoc($sql);
          }
          ?>
          <div class="details">
            <?php
            $fname_short = substr($row['fname'], 0, 2);

            $namer = $fname_short . '_' . $row['lname'] . '@' . $row['username'];
            ?>
            <span><?php echo $namer ?></span>
            <p><?php echo $row['status']; ?></p>
          </div>
        </div>

        <br>
        <br>

      </header>

      <div class="container mt-2">
        <div class="row">
          <div class="col">
            <a class="btn btn-outline-warning " href="php/logout.php?logout_id=<?php echo $row['unique_id']; ?>">Logout</a>

          </div>
          <div class="col">
           <a class="btn btn-outline-danger" href="php/delete_account.php?delete_id=<?php echo $row['unique_id']; ?>" 
           onclick="return confirm('Are you sure you want to delete your account? This cannot be undone.');">Delete Account</a>

          </div>
        </div>
      </div>

      <div class="search">
        <span class="text">Search for an user to start chat</span>
        <input type="text" placeholder="Enter name to search...">
        <button><i class="fas fa-search"></i></button>
      </div>
      <div class="users-list">

      </div>
    </section>
  </div>

  <script src="javascript/users.js"></script>

</body>

</html>