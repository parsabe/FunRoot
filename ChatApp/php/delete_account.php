<?php
session_start();
include_once "config.php";

if (isset($_GET['delete_id'])) {
    $user_id = mysqli_real_escape_string($conn, $_GET['delete_id']);

    // Delete the user
    $delete_query = mysqli_query($conn, "DELETE FROM users WHERE unique_id = '{$user_id}'");

    if ($delete_query) {
        // Optional: delete user-related files like profile images, etc.
        session_unset();
        session_destroy();
        header("Location: ../login.php");
        exit();
    } else {
        echo "Failed to delete account. Please try again.";
    }
} else {
    header("Location: ../users.php");
    exit();
}
?>
