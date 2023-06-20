Для начала хотелось бы поблагодарить ребят из [ultralytics](https://github.com/ultralytics) за открытый код и готовое решение с встроенным API.

# Модель

Итак, для решение задачи бралась новейшая и "лучшая" модель YOLOv8 на момент проекта:

![image](https://github.com/Fordreign/Tg_bot_detection_weed/assets/69246960/629b0624-b97b-4c95-b554-2bb1239eaef0)
картинка взята из [ресурса](https://github.com/ultralytics/ultralytics/issues/189)






# Метрики

**IoU**

![image](https://github.com/Fordreign/Tg_bot_detection_weed/assets/69246960/2dbfcd8d-265c-4a34-8b9c-d60373a902bf)
[resource](https://pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/)

Чтобы определить точность, нам нужно определить истинно положительные и ложно положительные результаты для обнаружения объектов. Истинно положительный результат определяется, когда IoU между предсказанной рамкой и истинной рамкой больше заданного порога IoU, тогда как ложно положительный результат имеет IoU ниже этого порога. Затем точность может быть определена как tp/(tp + fp).

![image](https://github.com/Fordreign/Tg_bot_detection_weed/assets/69246960/f56e950b-25ec-4e4d-a3f7-136211a5c231)

[resource](https://github.com/Fordreign/Tg_bot_detection_weed/assets/69246960/f56e950b-25ec-4e4d-a3f7-136211a5c231)

Для вычисления среднего среднего значения точности (mAP) мы выполняем следующие шаги:

Для каждого класса проводим оценку точности (AP) при различных порогах пересечения/объединения (IoU).
Мы начинаем с порога IoU 0,5 и постепенно увеличиваем его на 0,05 до достижения значения 0,95.
Для каждого порога IoU вычисляем точность (AP) для каждого класса.
Усредняем точности (AP) для каждого класса по всем порогам IoU, чтобы получить среднюю точность (AP) для этого класса.
Повторяем шаги 3-4 для каждого класса в наборе данных.
Усредняем средние точности (AP) для всех классов, чтобы получить mAP50-95.
Таким образом, mAP50-95 представляет собой среднюю точность по всем классам на интервале порогов IoU от 0,5 до 0,95 с шагом 0,05.


![image](https://github.com/Fordreign/Tg_bot_detection_weed/assets/69246960/978cd121-7b7f-4123-9b4a-09ee5ffd9659)

[resource]([x](https://blog.roboflow.com/mean-average-precision/))

Дальше для каждого класса считаем усредненный mAP.

![image](https://github.com/Fordreign/Tg_bot_detection_weed/assets/69246960/3a6da4e2-2fdd-45c9-82aa-873f350685c7)
