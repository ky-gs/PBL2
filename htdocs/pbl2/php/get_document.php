<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ducument Viewer</title>
</head>
<body>

<?php
// javascriptからファイルパスの取得
$docPath = $_GET['docPath'];
$imagePath = $_GET['imagePath'];
$articleId = isset($_GET['id']) ? $_GET['id'] : '';

// ファイルが存在するか確認
if (file_exists($docPath)) {
    $extension = pathinfo($docPath, PATHINFO_EXTENSION);

    // PDF ファイルの場合
    if ($extension == 'pdf') {
        // ファイルを直接表示
        echo '<div style="display: flex; justify-content: center; align-items: center; height: 100vh;">';
        echo '  <iframe src="' . $docPath . '" style="border: none; width: 100%; height: 100vh;"></iframe>';
        echo '</div>';
    } 
    // 画像ファイルの場合
    elseif ($extension == 'jpg' || $extension == 'jpeg' || $extension == 'png') {
        // 画像を表示
        echo '<div style="display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden;">';
        echo '  <img src="' . $docPath . '" style="object-fit: contain; width: 100%; height: 100%;" alt="Image">';
        echo '</div>';

    } 
    // その他のファイルの場合
    else {
        echo "Unsupported file format.";
    }
} else {
    $extension = pathinfo($imagePath, PATHINFO_EXTENSION);
    // 画像ファイルの場合
    if ($extension == 'jpg' || $extension == 'jpeg' || $extension == 'png') {
        // 画像を表示
        echo '<div style="display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden;">';
        echo '  <img src="' . $imagePath . '" style="object-fit: contain; width: 100%; height: 100%;" alt="Image">';
        echo '</div>';

    } 
    // その他のファイルの場合
    else {
        echo "Unsupported file format.";
    }
}

include 'db_connect.php'; // 接続ファイルを読み込む

// MySQLに接続
$conn = connectDB();

if (!empty($articleId)) {
    // PDFへのアクセス回数をカウント
    $updateQuery = "UPDATE access_log SET count = count + 1 WHERE id = ?";
    $stmt = $conn->prepare($updateQuery);
    $stmt->bind_param("i", $articleId);
    $stmt->execute();

    // データベース接続を閉じる
    $stmt->close();
    $conn->close();

    exit;
} else {
    echo 'Error: PDF path or ID not provided.';
    $conn->close();
}
?>

</body>
</html>

