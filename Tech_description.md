Для начала хотелось бы поблагодарить ребят из [ultralytics](https://github.com/ultralytics) за открытый код и готовое решение с встроенным API.
# Модель
![image](https://github.com/Fordreign/Tg_bot_detection_weed/assets/69246960/629b0624-b97b-4c95-b554-2bb1239eaef0)[ресурс](https://github.com/ultralytics/ultralytics/issues/189)

YOLOv8 состоит из двух основных компонентов:

Bottleneck (Основа):

Bottleneck  в YOLOv8 представляет собой модифицированный вариант Feature Pyramid Network (FPN).
Он выполняет операцию объединения признаков, используя skip-соединения между различными слоями сети.
Благодаря этому, информация о признаках с разных уровней сети объединяется, что позволяет лучше захватить пространственные и семантические информации на разных масштабах и разрешениях.

Head (Голова):

Голова в YOLOv8 отвечает за вывод предсказаний объектов на основе обработанных признаков из предыдущих модулей.
Она состоит из одной головы вывода (output head), которая предсказывает координаты ограничивающих рамок, вероятности классов и оценки уверенности (confidence scores), то есть 
<p float="midle">
  <img src="https://github.com/Fordreign/Detection_weed/assets/69246960/c3354205-d384-4bd7-ac24-6aa1dcb4be18" width="500" lendth=500 /> 
</p>
Голова использует механизм анкерных рамок (anchor boxes), который представляет собой предопределенные рамки с фиксированными размерами и соотношениями сторон. Модель предсказывает координаты анкерных рамок и корректирует их, чтобы точно соответствовать объекту на изображении.

# Метрики
**IoU**

![image](https://github.com/Fordreign/Tg_bot_detection_weed/assets/69246960/2dbfcd8d-265c-4a34-8b9c-d60373a902bf)
[resource](https://pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/)

Чтобы определить точность, нам нужно определить истинно положительные и ложно положительные результаты для обнаружения объектов. Истинно положительный (TP) результат определяется, когда IoU между предсказанной рамкой и истинной рамкой больше заданного порога IoU, тогда как ложно положительный (FP) результат имеет IoU ниже этого порога, а ложно отрицательный (FN), когда мы не попали предсказанной рамкой по истинной. . Затем точность может быть определена как TP/(TP + FP).

![image](https://github.com/Fordreign/Tg_bot_detection_weed/assets/69246960/f56e950b-25ec-4e4d-a3f7-136211a5c231)

[resource](https://github.com/Fordreign/Tg_bot_detection_weed/assets/69246960/f56e950b-25ec-4e4d-a3f7-136211a5c231)

Для вычисления среднего среднего значения точности (mAP) мы выполняем следующие шаги:

Для каждого класса проводим оценку точности (AP) при различных порогах пересечения/объединения (IoU).
* Мы начинаем с порога IoU 0,5 и постепенно увеличиваем его на 0,05 до достижения значения 0,95.
* Для каждого порога IoU вычисляем точность (AP) для каждого класса.
* Усредняем точности (AP) для каждого класса по всем порогам IoU, чтобы получить среднюю точность (AP) для этого класса.

Ниже видео для общего понимания

[AP](https://github.com/Fordreign/Tg_bot_detection_weed/assets/69246960/66d13ac0-fb24-4850-88a2-31c019805147)

[resource](https://blog.roboflow.com/mean-average-precision/)

Для mAP50-95:

* Повторяем шаги 3-4 для каждого класса в наборе данных.
* Усредняем средние точности (AP) для всех классов, чтобы получить mAP50-95.
* Таким образом, mAP50-95 представляет собой среднюю точность по всем классам на интервале порогов IoU от 0,5 до 0,95 с шагом 0,05.

![image](https://github.com/Fordreign/Tg_bot_detection_weed/assets/69246960/3a6da4e2-2fdd-45c9-82aa-873f350685c7)
# Функции потерь
Функция потерь для модели YOLOv8 состоит из трех частей: потери рамки, потери классификации и потери распределения фокуса. Давайте рассмотрим каждую часть по отдельности:

Потеря рамки (box loss):

Эта часть функции потерь оценивает, насколько точно модель предсказывает рамку, ограничивающую объект.
Она использует понятие IoU (пересечение по площади / объединение по площади), чтобы сравнить предсказанную рамку с истинной рамкой объекта.
Чем меньше расхождение между предсказанной и истинной рамкой (чем выше IoU), тем меньше будет потеря рамки.

Потеря классификации (classification loss):

Эта часть функции потерь оценивает, насколько точно модель предсказывает класс объекта в каждой ячейке сетки.
Она использует бинарную перекрестную энтропию для сравнения предсказанной вероятности класса с истинной меткой класса.
Чем меньше расхождение между предсказанной вероятностью и истинной меткой класса, тем меньше будет потеря классификации.

Потеря распределения фокуса (distribution focal loss):

Эта часть отвечает за обучение модели предсказывать объекты разных размеров и ориентаций.
Она включает в себя два компонента: первый компонент измеряет разницу между предсказанными значениями IoU для соседних рамок объекта, а второй компонент измеряет разницу между предсказанными значениями IoU их соседей для каждой ячейки сетки.

Каждая часть функции потерь вносит свой вклад в общую потерю модели, и цель состоит в том, чтобы минимизировать эту общую потерю путем обучения модели на обучающих данных.


L = <sup>λ<sub>box</sub></sup>&frasl;<sub>N<sub>pos</sub></sub> &sum;<sub>x,y</sub> (1<sub>c∗</sub>x,y * (1−q<sub>x,y</sub> + 
(k<sub>b</sub>x,y − ˆb<sub>x,y</sub>)<sup>2</sup> &frasl; ρ<sup>2</sup>) + α<sub>x,y</sub>ν<sub>x,y</sub>) "box_loss"
 
 +<sup>λ<sub>cls</sub></sup>&frasl;<sub>N<sub>pos</sub></sub> &sum;<sub>x,y</sub> &sum;<sub>c∈classes</sub> (y<sub>c</sub> * log(ˆy<sub>c</sub>) +(1 − y<sub>c</sub>) * log(1 − ˆy<sub>c</sub>))       "cl_loss"
 
 +<sup>λ<sub>df l</sub></sup>&frasl;<sub>N<sub>pos</sub></sub> &sum;<sub>x,y</sub> (1<sub>c∗</sub>x,y * h * (− (q<sub>x,y</sub>+1 − q<sub>x,y</sub>) * log(ˆq<sub>x,y</sub>) + (q<sub>x,y</sub> − q<sub>x,y</sub>−1) * log(ˆq<sub>x,y</sub>+1))) "dfl_loss"
<p>where:</p>
<ul>
  <li>qx,y = IoUx,y = <sup>βˆx,y ∩ βx,y</sup>&frasl;<sub>βˆx,y ∪ βx,y</sub></li>
  <li>νx,y = <sup>4π</sup>&frasl;<sub>2</sub> (arctan(<sup>wx,y</sup>&frasl;<sub>hx,y</sub>) − arctan(<sup>wˆx,y</sup>&frasl;<sub>hˆx,y</sub>))<sup>2</sup></li>
  <li>αx,y = <sup>ν</sup>&frasl;<sub>1 − qx,y</sub></li>
  <li>yˆc = σ(·)</li>
  <li>qˆx,y = softmax(·)</li>
</ul>

# Алгоритм обучения 
YOLOv8 имеет несколько разновидностей: 
<div class="md-typeset__table"><table>
<thead>
<tr>
<th>Model</th>
<th>size<br><sup>(pixels)</sup></th>
<th>mAP<sup>val<br>50-95</sup></th>
<th>Speed<br><sup>CPU ONNX<br>(ms)</sup></th>
<th>Speed<br><sup>A100 TensorRT<br>(ms)</sup></th>
<th>params<br><sup>(M)</sup></th>
<th>FLOPs<br><sup>(B)</sup></th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt">YOLOv8n</a></td>
<td>640</td>
<td>37.3</td>
<td>80.4</td>
<td>0.99</td>
<td>3.2</td>
<td>8.7</td>
</tr>
<tr>
<td><a href="https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt">YOLOv8s</a></td>
<td>640</td>
<td>44.9</td>
<td>128.4</td>
<td>1.20</td>
<td>11.2</td>
<td>28.6</td>
</tr>
<tr>
<td><a href="https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt">YOLOv8m</a></td>
<td>640</td>
<td>50.2</td>
<td>234.7</td>
<td>1.83</td>
<td>25.9</td>
<td>78.9</td>
</tr>
<tr>
<td><a href="https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8l.pt">YOLOv8l</a></td>
<td>640</td>
<td>52.9</td>
<td>375.2</td>
<td>2.39</td>
<td>43.7</td>
<td>165.2</td>
</tr>
<tr>
<td><a href="https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt">YOLOv8x</a></td>
<td>640</td>
<td>53.9</td>
<td>479.1</td>
<td>3.53</td>
<td>68.2</td>
<td>257.8</td>
</tr>
</tbody>
</table></div>

Для данного проекта выбиралась "наилучшая" по mAP и параметрам YOLOv8x

Конечно можно использовать полегче модели, если у нас нехватает мощностей для инференса и дальнейшей передачи сигнала опрыскивателю и другим подключенным системам.

*Подбор гиперпараметров*: для этой процедуры требуется значительное количество ресурсов и времени. Если мы используем поиск по сетке (grid search) для нахождения гиперпараметров и учитываем, что у модели около 20 гиперпараметров, а обучение на любом из наших датасетов займет около 60 минут на 30 эпох, то такой поиск колоссально затратен по времени и ресрсам. Поэтому я решил выбрать "оптимально-базовые" гиперпараметры на основе своего опыта и анализа работ в научных статьях.

Но все же я решил проверить , какая модель себя приэтом проявит лучше.
Изначально YOLOv8 предобучена на [COCO](https://cocodataset.org/#home) где порядка 80+ классов и 330к+ изображений разного размера и качества.

**Эксперимет №1.**
Обучим YOLOv8x на [WeedCrop Image Dataset](https://www.kaggle.com/datasets/vinayakshanawad/weedcrop-image-dataset), затем сохраняем веса модели и снова цикл обучения уже на [LincoInBeet](https://datasets.activeloop.ai/docs/ml/datasets/lincolnbeet-dataset/#lincoinbeet-dataset).

**Эксперимет №2.**


# Cituation
[arxiv](https://arxiv.org/pdf/2305.09972.pdf)
