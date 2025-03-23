# Определить пути к директориям
$results = "./allure-files"
$rep_history = "./allure-report/history"
$report = "./allure-report"

# Удалить папку с результатами
Remove-Item -Recurse -Force $results

# Запустить тесты и сохранить результаты в $results
pytest --alluredir=$results

# Скопировать историю в результаты
Copy-Item -Recurse -Force $rep_history $results

# Удалить старый отчет
Remove-Item -Recurse -Force $report

# Сгенерировать новый отчет Allure
allure generate $results -o $report

# Открыть отчет Allure
allure open $report
