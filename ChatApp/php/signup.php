<?php
session_start();
include_once "config.php";
$fname = mysqli_real_escape_string($conn, $_POST['fname']);
$lname = mysqli_real_escape_string($conn, $_POST['lname']);
$username = mysqli_real_escape_string($conn, $_POST['username']);
$password = mysqli_real_escape_string($conn, $_POST['password']);
$date = date("d M Y H:i:s");
if (!empty($fname) && !empty($lname) && !empty($password)) {

    $sql = mysqli_query($conn, "SELECT * FROM users WHERE username = '{$username}'");
    if (mysqli_num_rows($sql) > 0) {
        echo "$email - This username already exist!";
    } else {

        $time = time();

        $ran_id = rand(time(), 10000);
        $status = "Online";
        $encrypt_pass = md5($password);
        $insert_query = mysqli_query($conn, "INSERT INTO users (unique_id, fname, lname, username, password, status, date)
                                VALUES ({$ran_id}, '{$fname}','{$lname}', '{$username}', '{$encrypt_pass}', '{$status}', '{$date}')");
        if ($insert_query) {
            $select_sql2 = mysqli_query($conn, "SELECT * FROM users WHERE username = '{$username}'");
            if (mysqli_num_rows($select_sql2) > 0) {
                $result = mysqli_fetch_assoc($select_sql2);
                $_SESSION['unique_id'] = $result['unique_id'];
                echo "success";
            } else {
                echo "This username not Exist!";
            }
        } else {
            echo "Something went wrong. Please try again!";
        }
    }
} else {
    echo "Fields cannot be empty";
}
