<?php
function connectDB() {
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "pbl2";

    // MySQLに接続
    $conn = new mysqli($servername, $username, $password, $dbname);

    // 接続エラーの確認
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    return $conn;
}
?>
