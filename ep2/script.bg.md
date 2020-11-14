# Minimum Coin Change Problem
## Ресто с най-малък брой монети

Coin change problem или как да върнем ресто с най-малък брой монети е интересна задача с елегантно решение, която използва техниката _динамично програмиране_.

Задачата е следната: имаме конкретна сума пари, която трябва да върнем. За по-лесно, нека превърнем сумата до такава само в стотинки. Разполагаме с монети от всяка деноминация (т.е. имаме монети от 1, 2, 5, 10, и т.н стотинки). Целта е да я разбием на монети, така че броят на монетите да бъде възможно най-малък. 

Задачата може да се реши с brute force (или на български метода на "грубата сила") - с други думи да пробваме всички комбинации от монети, с които може да представим сумата и да изберем тази комбинация, която има най-малко монети. Това е валидно, но крайно неефективно решение.

Друга стратегия би била да избираме най-голямата деноминация, която ни доближава най-бързо до желаната сума. Този алгоритъм се нарича _greedy_ (или на български _алчен_). Това не винаги е най-опитмалната стратегия. Представете си, че разполагаме с монети от 1, 5, 10, 20, 25 стотинки, а трябва да върнем 40 стотинки. Алчения алгоритъм ще ни даде решение от 3 монети - 25, 10, 5, докато оптималното би било - само от 2 монети - от 2 по 20 стотинки 

За щастие задачата им _optimal substructure_ (или на български _оптимална подструктура_). Това означава, че ако разбием задачата на по-малки и намерим оптималното решение за всяка от тях, това е оптималното решение и на голямата задача.

Нека дадем пример с нашата задача. Да предположим, че сумата, която искаме да върнем е 13 стотинки. Разполагаме с монети от 1, 2, 5. Можем да разбием задачата на 3 подзадачи:

### Минимално ресто от 13 стотинки
1. Взимаме 1 монета от 1 стотинка + минималния брой монети, които са необходими да преставим 12 стотинки (13 - 1) 
2. Взимаме 1 монета от 2 стотинка + минималния брой монети, които са необходими да преставим 11 стотинки (13 - 2)
3. Взимаме 1 монета от 5 стотинка + минималния брой монети, които са необходими да преставим 8 стотинки (13 - 5)

### Минимално ресто от 12 стотинки
1. Взимаме 1 монета от 1 стотинка + минималния брой монети, които са необходими да преставим 11 стотинки (12 - 1) 
2. Взимаме 1 монета от 2 стотинка + минималния брой монети, които са необходими да преставим 10 стотинки (12 - 2)
3. Взимаме 1 монета от 5 стотинка + минималния брой монети, които са необходими да преставим 7 стотинки (12 - 5)

### Минимално ресто от 11 стотинки
1. Взимаме 1 монета от 1 стотинка + минималния брой монети, които са необходими да преставим 10 стотинки (11 - 1) 
2. Взимаме 1 монета от 2 стотинка + минималния брой монети, които са необходими да преставим 9 стотинки (11 - 2)
3. Взимаме 1 монета от 5 стотинка + минималния брой монети, които са необходими да преставим 6 стотинки (11 - 5)

Продължаваме, така докато стигнем до ресто, което може да се изрази само с една монета.

Може би забелязахте, че често ни се налагаше да решаваме една и съща подзадача: примерно тук - минимално ресто от 10 и 11 стотинки. 

С помощта на техниката dynamic programming или на български _динамично програмиране_  ще си спестим постоянното пресмятане на една и съща сума. Динамичното програмиране е въведено от американския математик Ричард Ърнест Белман през 1953-та година. Ще се опитам да обясня принципа нетехнически на дъщеря ми, която е на 14 години.

- Александра, колко елхички виждаш на екрана?
- 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 
- Добре. А сега ще добавя още една. Колко станаха?
- Ами 12, много ясно.
- Как успя да ги преброиш толкова бързо?
- Не съм ги броила! Запомних, че има 11 и като добавим още 1 стават 12.
- Супер - това е динамично програмиране: да запомним някъде резултата от предишна подзадача и да си спестим усилието при решаването на задачата, която я включва. 

Ето как ще приложим тази техника за решаване ефективно на задачата. Ще си създадем един един масив, с размер с единица по-голям от сумата, която търсим - в този случай с 14 кутийки за сума от 13 стотинки. Във всяка клетка ще записваме минималния брой монети, които са необходими за да се достигне конкретната сума. В началото всички клетки са инициализирани с безкрайност - т.е. още първия конкретен брой монети ще бъде прието като потенциално решение. Във втори масив ще пазим монетата, с която сме постигнали минимален брой за конкретната сума. Той ще ни позволи да възпроизведем редицата от монети, които са довели до минималната сума.

Започваме със сума 0, която не може да се представи с монети - т.е. броя на монетите, които я представят е 0.

Следващата сума е 1. Пробваме всяка от 3-те монети, които имаме. 2 и 5 не можем да използваме защото дават отрицателна сума. Следователно минималния брой за сума от 1 е 1 монета.

Следващата сума е 2. Пробваме пак 3-те монети. 5 не може да ползваме, остават 1 и 2. Ако използваме монета от 1 стотинка, то трябва да видим колко монети са необходими за постигане на сума 1. Това е 1 една монета. Следователно минималния брой монети ако изберем 1 стотинка е 2 (1 монета за сума 1 плюс 1 (текущата)). Ако използваме монета от 2 стотинки, то трябва да видим колко монети са необходими за сума 0. Това са нула монети. Следователно минималния брой монети ако изберем 2 стотинки е 1 (0 монети за сума 0 плюс 1 (текущата)). С монета от 2 стотинки постигаме най-малък брой монети за сума от 2 (само 1 монета), затова записваме нея.

Следващата сума е 3. Пробваме пак 3-те монети. 5 все още не може да ползваме, остават 1 и 2. Ако използваме монета от 1 стотинка, трябва да видим колко монети са необходими за постигане на сума от 2 стотинки.  



# Източници
* https://algorithmist.com/wiki/Min-Coin_change
* https://en.wikipedia.org/wiki/Optimal_substructure
* https://medium.com/@trykv/how-to-solve-minimum-coin-change-f96a758ccade


