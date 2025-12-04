// dateOption.js

// 年の選択肢を生成する関数
function generateYearOptions(startYear, endYear, selectElement) {
    for (let year = startYear; year <= endYear; year++) {
        const option = document.createElement('option');
        option.value = year;
        option.text = year;
        selectElement.appendChild(option);
    }
}

// 月の選択肢を生成する関数
function generateMonthOptions(selectElement) {
    for (let month = 1; month <= 12; month++) {
        const option = document.createElement('option');
        const formattedMonth = month < 10 ? '0' + month : '' + month;
        option.value = formattedMonth;
        option.text = formattedMonth;
        selectElement.appendChild(option);
    }
}

// 日の選択肢を生成する関数
function generateDayOptions(selectElement) {
    for (let day = 1; day <= 31; day++) {
        const option = document.createElement('option');
        const formattedDay = day < 10 ? '0' + day : '' + day;
        option.value = formattedDay;
        option.text = formattedDay;
        selectElement.appendChild(option);
    }
}

// 年月日の選択肢を生成
generateYearOptions(2023, 2024, document.getElementById('ageStartYear'));
generateMonthOptions(document.getElementById('ageStartMonth'));
generateDayOptions(document.getElementById('ageStartDay'));

// ageEndのデフォルト値を設定（2024-12-31）
const endYearSelect = document.getElementById('ageEndYear');
const endMonthSelect = document.getElementById('ageEndMonth');
const endDaySelect = document.getElementById('ageEndDay');

generateYearOptions(2023, 2024, document.getElementById('ageEndYear'));
generateMonthOptions(document.getElementById('ageEndMonth'));
generateDayOptions(document.getElementById('ageEndDay'));

// デフォルト値を設定
endYearSelect.value = '2024';
endMonthSelect.value = '12';
endDaySelect.value = '31';

// 画面上でもデフォルト値を反映
document.getElementById('ageEndYear').value = endYearSelect.value;
document.getElementById('ageEndMonth').value = endMonthSelect.value;
document.getElementById('ageEndDay').value = endDaySelect.value;