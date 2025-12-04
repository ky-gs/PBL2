<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

include 'db_connect.php'; // 接続ファイルを読み込む

// MySQLに接続
$conn = connectDB();

// クエリの実行
// 入力データの取得
$keyword = $_GET['keyword'];
$categories = isset($_GET['categories']) ? explode(',', $_GET['categories']) : [];
$keywordLogic = $_GET['keywordLogic'];
$bond = $_GET['bond'];
$regions = isset($_GET['regions']) ? explode(',', $_GET['regions']) : [];
$ageStart = $_GET['ageStart'];
$ageEnd = $_GET['ageEnd'];
$number = $_GET['number'];

// SQL クエリの構築
$sql = "SELECT id, title, article, date, page, page_number, file_name, picture, chart, advertising FROM article WHERE ";

// キーワード検索条件の追加
$keywords = mb_split('[\s　]+', $keyword);
$likeConditions = [];
foreach ($keywords as $kw) {
    $likeConditions[] = "(title LIKE '%$kw%' OR keitaiso LIKE '%$kw%')";
}

// キーワード論理演算子の追加
$sql .= $keywordLogic == 'AND' ? implode(' AND ', $likeConditions) : implode(' OR ', $likeConditions);

// カテゴリ検索条件の追加
if (!empty($categories)) {
    if ($bond == 'AND') {
        // AND検索の場合は全てのカテゴリを含む記事を取得
        $sql .= "AND id IN (SELECT article_id FROM article_tags WHERE tag_id IN (" . implode(',', $categories) . ") GROUP BY article_id HAVING COUNT(DISTINCT tag_id) = " . count($categories) . ") ";
    } else {
        // OR検索の場合はいずれかのカテゴリを含む記事を取得
        $sql .= "AND id IN (SELECT DISTINCT article_id FROM article_tags WHERE tag_id IN (" . implode(',', $categories) . ")) ";
    }
}

// $regionsが空でない場合、条件を組み立てる
if (!empty($regions)) {
    // implode関数を使用して、$regionsの要素を「OR」で連結
    $regionCondition = implode(' OR ', array_map(function($region) {
        // 各要素に対して「area_id = $region」を適用
        return "area_id = $region";
    }, $regions));

    // 完成した条件をSQLクエリに組み込む
    $sql .= " AND ($regionCondition) ";
}

if ($ageStart != '' && $ageEnd != '') {
    $sql .= " AND date BETWEEN '$ageStart' AND '$ageEnd' ";
}

// ソートの条件を追加
$sortOrder = $_GET['sortOrder'] === 'asc' ? 'ASC' : 'DESC';
$sql .= "ORDER BY date $sortOrder ";

// 表示数の制限
$sql .= "LIMIT $number";

// SQL クエリの実行
$result = $conn->query($sql);

// エラーチェック
if (!$result) {
    die('Query error: ' . $conn->error);
}

// 結果の取得
if ($result->num_rows > 0) {
    $data = array();

    while ($row = $result->fetch_assoc()) {
        // date, page, number_in_page, file_name からデータパスを生成
        list($year, $month, $day) = explode("-", $row['date']);
        $doc_path = '';
        $image_path = '';
        $chart_path = '';
        $advertising_path = '';
        // pdfのパス
        if ($row['file_name'] !== NULL) {
            $doc_path = '../jomo/' . $year . '/' . $month . '/' . $day . '/' . $row['page'] . '/' . $row['page_number'] . '/' . $row['file_name'];
        } else {
            // file_name が存在しない場合は他のパスを代用する
            if ($row['picture'] !== NULL) {
                $doc_path = '../jomo/' . $year . '/' . $month . '/' . $day . '/' . $row['page'] . '/' . $row['page_number'] . '/' . $row['picture'];
            } elseif ($row['chart'] !== NULL) {
                $doc_path = '../jomo/' . $year . '/' . $month . '/' . $day . '/' . $row['page'] . '/' . $row['page_number'] . '/' . $row['chart'];
            } elseif ($row['advertising'] !== NULL) {
                $doc_path = '../jomo/' . $year . '/' . $month . '/' . $day . '/' . $row['page'] . '/' . $row['page_number'] . '/' . $row['advertising'];
            } else {
                // すべてない場合はデフォルト画像のパスを代入
                $doc_path = '../img/default.png';
            }
        }
        // 画像のパス    
        if ($row['picture'] !== NULL) {
            $image_path = '../jomo/' . $year . '/' . $month . '/' . $day . '/' . $row['page'] . '/' . $row['page_number'] . '/' . $row['picture'];
            // $raw_image = file_get_contents($image_path);
        } else {
            // picture が存在しない場合は他のパスを代用する
            if ($row['chart'] !== NULL) {
                $image_path = '../jomo/' . $year . '/' . $month . '/' . $day . '/' . $row['page'] . '/' . $row['page_number'] . '/' . $row['chart'];
                // $raw_image = file_get_contents($image_path);
            } elseif ($row['advertising'] !== NULL) {
                $image_path = '../jomo/' . $year . '/' . $month . '/' . $day . '/' . $row['page'] . '/' . $row['page_number'] . '/' . $row['advertising'];
                // $raw_image = file_get_contents($image_path);
            } else {
                // すべてない場合はデフォルト画像のパスを代入
                $image_path = '../img/default.png';
            }
        }

        $raw_image = file_get_contents($image_path);

        if ($row['article'] !== NULL) {
            $original_text = $row['article'];
        } else {
            $original_text = '';
        }

        $data[] = array(
            'id' => $row['id'],
            'title' => $row['title'],
            'original_text' => mb_substr($original_text, 0, 100, 'UTF-8'),
            'date' => $row['date'],
            'docPath' => $doc_path,
            'imagePath' => $image_path,
            'image' => base64_encode($raw_image),
        );
    }

    // JSON 形式で検索結果を出力
    echo json_encode($data);

} else {
    // 検索結果がない場合
    echo json_encode(array(
        array(
            'title' => 'None_Title',
            'original_text' => 'None_text',
            'date' => 'None_date',
            'doc_path' => 'None_path',
            'image' => 'None_image',
        )
    ));
}

// echo $sql;

// MySQL接続を閉じる
$conn->close();
?>