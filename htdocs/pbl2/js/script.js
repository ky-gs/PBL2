document.addEventListener('DOMContentLoaded', async function() {
    // カテゴリのチェックボックスの変更イベントを設定
    var categoryCheckboxes = document.querySelectorAll('input[name="tag[]"]');
    categoryCheckboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', handleSearch);
    });

    // カテゴリ用の論理演算子の選択ラジオボタンの変更イベントを設定
    var bondRadioButtons = document.querySelectorAll('input[name="bond"]');
    bondRadioButtons.forEach(function(radio) {
        radio.addEventListener('change', handleSearch);
    });

    // キーワード用の論理演算子の選択ラジオボタンの変更イベントを設定
    var keywordLogicRadioButtons = document.querySelectorAll('input[name="keywordLogic"]');
    keywordLogicRadioButtons.forEach(function(radio) {
        radio.addEventListener('change', handleSearch);
    });

    // 地域の選択の変更イベントを設定
    var regionCheckboxes = document.querySelectorAll('input[name="regions[]"]');
    regionCheckboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', handleSearch);
    });

    // 年代の選択の変更イベントを設定
    document.getElementById('ageStartYear').addEventListener('change', handleSearch);
    document.getElementById('ageStartMonth').addEventListener('change', handleSearch);
    document.getElementById('ageStartDay').addEventListener('change', handleSearch);

    document.getElementById('ageEndYear').addEventListener('change', handleSearch);
    document.getElementById('ageEndMonth').addEventListener('change', handleSearch);
    document.getElementById('ageEndDay').addEventListener('change', handleSearch);

    // 表示数の選択の変更イベントを設定
    document.getElementById('number').addEventListener('change', handleSearch);

    // ソートの選択の変更イベントを設定
    document.getElementById('sortOrder').addEventListener('change', handleSearch);

    // 検索ボタンのクリックイベントを設定
    document.getElementById('searchBtn').addEventListener('click', handleSearch);

    // キーワード入力窓にEnterキーのイベントリスナーを追加
    document.getElementById('searchInput').addEventListener('keydown', function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            handleSearch();
        }
    });
    handleSearch();
});

// カテゴリ変更やキーワード検索に対する処理を統一化
function handleSearch() {
    // 入力されたキーワードを取得
    var keyword = document.getElementById('searchInput').value;
    // 非同期処理を待ってから検索APIの呼び出し
    processKeyword(keyword)
        .then(processedKeyword => {
            // 選択されたカテゴリを取得
            var selectedCategories = [];
            var checkedCheckboxes = document.querySelectorAll('input[name="tag[]"]:checked');
            checkedCheckboxes.forEach(function(checkedCheckbox) {
                selectedCategories.push(checkedCheckbox.value);
            });

            //　キーワードの論理演算子を取得
            var selectedKeywordLogic = document.querySelector('input[name="keywordLogic"]:checked').value;

            // カテゴリの論理演算子を取得
            var selectedBond = document.querySelector('input[name="bond"]:checked').value;

            // 選択された地域を取得
            var selectedRegions = [];
            var regionCheckboxes = document.querySelectorAll('input[name="regions[]"]:checked');
            regionCheckboxes.forEach(function(checkbox) {
                    selectedRegions.push(checkbox.value);
            }); 

            // 選択された年代を取得
            var selectedAgeStart = document.getElementById('ageStartYear').value + '-' + document.getElementById('ageStartMonth').value + '-' + document.getElementById('ageStartDay').value;
            var selectedAgeEnd = document.getElementById('ageEndYear').value + '-' + document.getElementById('ageEndMonth').value + '-' + document.getElementById('ageEndDay').value;

            // 選択されたソート順を取得
            var selectedSortOrder = document.getElementById('sortOrder').value;

            // 表示する記事の数を取得
            var selectedNumber = document.getElementById('number').value;

            // 検索APIの呼び出し
            search(processedKeyword, selectedCategories, selectedKeywordLogic, selectedBond, selectedRegions, selectedAgeStart, selectedAgeEnd, selectedSortOrder, selectedNumber);

            // コンソールにメッセージを表示（デバッグ用）
            console.log('Search initiated. Keyword: ' + processedKeyword +
                ', Selected Categories: ' + selectedCategories +
                ', Selected Keyword Logic: ' + selectedKeywordLogic +
                ', Selected Bond: ' + selectedBond +
                ', Selected Regions: ' + selectedRegions +
                ', Selected Age Start: ' + selectedAgeStart +
                ', Selected Age End: ' + selectedAgeEnd +
                ', Selected Sort Order: ' + selectedSortOrder +
                ', Selected Number: ' + selectedNumber);
        })
        .catch(error => {
            console.error("Error processing keyword:", error);
        });
}

// 検索APIの実行
function search(processedKeyword, selectedCategories, selectedKeywordLogic, selectedBond, selectedRegions, selectedAgeStart, selectedAgeEnd, selectedSortOrder, selectedNumber) {
    // PHPファイルへの非同期通信
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            displaySearchResults(data);
            console.log(this.responseText);
        }
    };

    // カテゴリの選択情報、形式の選択情報、地域の選択情報、年代の選択情報、表示数の選択情報をクエリ文字列に組み込む
    var categoryQueryString = selectedCategories.length > 0 ? '&categories=' + encodeURIComponent(selectedCategories.join(',')) : '';
    var keywordLogicQueryString = '&keywordLogic=' + encodeURIComponent(selectedKeywordLogic);
    var bondQueryString = '&bond=' + encodeURIComponent(selectedBond);
    var regionQueryString = selectedRegions.length > 0 ? '&regions=' + encodeURIComponent(selectedRegions.join(',')) : '';
    var ageStartQueryString = selectedAgeStart ? '&ageStart=' + encodeURIComponent(selectedAgeStart) : '';
    var ageEndQueryString = selectedAgeEnd ? '&ageEnd=' + encodeURIComponent(selectedAgeEnd) : '';
    var sortOrderQueryString = '&sortOrder=' + encodeURIComponent(selectedSortOrder);
    var numberQueryString = '&number=' + encodeURIComponent(selectedNumber);

    xhttp.open("GET", "./php/query.php?keyword=" + encodeURIComponent(processedKeyword) + keywordLogicQueryString + categoryQueryString + bondQueryString + regionQueryString + ageStartQueryString + ageEndQueryString + sortOrderQueryString + numberQueryString, true);
    xhttp.send();
}

// 検索結果を表示する関数
function displaySearchResults(data) {
    var resultArea = document.getElementById("searchResults");

    // テーブルをクリア
    resultArea.innerHTML = "";

    if (data[0].title === 'None_Title' && data[0].original_text === 'None_text') {
        // 検索結果がない場合のメッセージを表示
        resultArea.innerHTML = '<p>No matching results.</p>';
    } else {
        data.forEach(function (row) {
            // タイトル（リンク付き）の作成
            var titleElement = document.createElement('h2');
            titleElement.classList.add('result-title');
            titleElement.classList.add('left-section');
            var titleLink = document.createElement('a');

            // PHPファイルへのパスを指定
            var phpFilePath = './php/get_document.php'; 

            // パラメータを指定
            var articleId = row.id; // rowオブジェクトからidを取得する
            var docPath = row.docPath;
            var imagePath = row.imagePath;
            var docUrl = phpFilePath + '?docPath=' + encodeURIComponent(docPath)+ '&id=' + encodeURIComponent(articleId) + '&imagePath=' + encodeURIComponent(imagePath) ;

            titleLink.href = docUrl; // docのURL
            titleLink.textContent = row.title;
            titleElement.appendChild(titleLink);

            // Original Text の作成
            var originalTextElement = document.createElement('p');
            originalTextElement.classList.add('result-text'); 
            originalTextElement.classList.add('left-section');
            originalTextElement.textContent = row.original_text;

            titleElement.appendChild(originalTextElement);

            // Date の作成
            var dateElement = document.createElement('span');
            dateElement.classList.add('result-date'); 
            dateElement.classList.add('right-section');
            dateElement.textContent = row.date;

            // 画像の作成
            var imageElement = document.createElement('img');
            imageElement.classList.add('result-image');
            imageElement.classList.add('right-section');
            imageElement.src = 'data:image/jpeg;base64,' + row.image; // 画像データのBase64エンコード

            dateElement.appendChild(imageElement);

            // タイトル、Original Text、Date をまとめるコンテナ
            var resultContainer = document.createElement('div');
            resultContainer.classList.add('search-result'); 

            resultContainer.appendChild(titleElement);
            // resultContainer.appendChild(originalTextElement);
            resultContainer.appendChild(dateElement);
            // resultContainer.appendChild(imageElement);

            // 検索結果表示エリアに追加
            resultArea.appendChild(resultContainer);
        });
    }
}

function processKeyword(keyword) {
    const DICT_PATH = "./dict";

    return new Promise((resolve, reject) => {
        // Kuromoji
        kuromoji.builder({dicPath: DICT_PATH}).build((err, tokenizer) => {
            if (err) {
                reject(err);
                return;
            }

            const tokens = tokenizer.tokenize(keyword); 
            const relevantWords = tokens.filter(token => ['名詞', '動詞', '形容詞', '副詞', '助詞', '感動詞'].includes(token.pos));

            const baseForms = relevantWords.map(token => token.basic_form || token.surface_form);

            const processedKeyword = baseForms.join(' ');
            resolve(processedKeyword);
        });
    });
}