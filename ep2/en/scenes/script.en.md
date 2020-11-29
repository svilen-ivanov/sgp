# Minimum Coin Change Problem
## Ресто с най-малък брой монети


Coin change problem is essential to computer science. I has an elegant solution that demonstrates the technique _dynamic programming_.


The task is as following: there is a specific amount of money. To make it easier, let's turn that amount into cents. We have coins of each denomination (for example we have coins of 1, 2, 5, 10, etc. cents). The goal is to find the smallest possible number of coins that add up to that amount.

The task can be solved with brute force approach. We can try all possible combinations of coins that add up to the amount and pick the combination with least number of coins. This is a valid albeit highly inefficient approach.

Another way to solve the problem is to pick the largest denomination that brings us closest to the desired amount. This algorithm is called _greedy_. However this is not always the most optimal strategy. Let's say we have coins of 1, 5, 10, 20, 25 cents, and we have to return 40 cent change. A greedy algorithm will give us a solution of 3 coins - 25, 10, 5, while the optimal would be - only 2 coins of 20 cents. 

Luckily, the task exhibits an _optimal substructure_. It means that if we break down the problem into smaller ones and find the optimal solution for each of them, a combination of these optimal solutions is the optimal solution of the task.

Let's see this property with an example. There are coins of 1, 2 and 5 cents. The amount we want to return as change is 9 cents.

We try each coin and subtract it from the amount. We get a difference which in turn we break down further with a minimum number of coins. Afterwards we compare each coin result, and the  smallest number of the 3 is the solution to the problem.
  As for the subtasks, we continue to solve them in the same way. Let's break down the subtask for 8 cents. Again, we have 3 options, and we have to compute each of them separately and see which one gives the least solution.

We continue with the solution of the subtask for 7 cents. Again we have 3 options. We continue with the solution of the subtask for 4 cents. This time we have only 2 options because we cannot express 4 cents with 5 cent coins.

You probably may have noticed that we often have to solve the same subtask: the task for 7, 6, 3 and 2 cents is repeated.

С помощта на техниката dynamic programming или на български _динамично програмиране_  ще си спестим постоянното пресмятане на една и съща сума. Динамичното програмиране е въведено от американския математик Ричард Ърнест Белман през 1953-та година. Ще се опитам да обясня принципа нетехнически на дъщеря ми, която е на 14 години.

- Али, колко монетки виждаш на екрана?
- 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 
- Добре. А сега ще добавя още една. Колко станаха?
- Ами 12, много ясно.
- Как успя да ги преброиш толкова бързо?
- Не съм ги броила! Запомних, че има 11 и като добавим още 1 стават 12.
- Супер - това е динамично програмиране: да запомним някъде резултата от предишна подзадача и да си спестим усилието при решаването на задачата, която я включва. 

Ето как ще приложим тази техника за ефективно решаване на задачата на езика Python.

Ще си създадем един един списък, с размер с единица по-голям от сумата, която търсим - в този случай с 10 клетки за сума от 9 стотинки. Всеки един индекс в масива представлява подсума, а стойността му - минималния брой монети за да се достигне. Крайното решение на задачата ще се намира в последната клетка на масива. Във втори списък ще пазим монетата, с която сме постигнали тази сума. Той ще ни позволи да възпроизведем редицата от монети, които са довели до минималната сума.

Започваме с подсума 0 която не може да се изрази с монети. 

Започваме да пресмятаме броя на монетите за всяка една подсума докато стигнем до сумата, която търсим. Ще пробваме със всяка от монетите, като използваме изчисленията от предишните итерации. Така лесно ще намерим, с коя от 3-те монети достигаме до минимален брой. След това ще го запишем в масива и ще го използваме в следващите итерации или за намиране на крайното решение. 

В долната част на екрана можете да видите как се променят променливите при изпълнение на програмата. Постарал съм се имената на променливите да са максимално описателни (а не n, i, j, k) за максимално улеснение.

Като самостоятелна работа, опитайте се да отговорите на следните въпроси във коментарите:
* коя е точно поредицата от монети, която дава търсената сума?
* защо някои променливи или списъци са инициализирани с None, а други с безкрайност?
* какво означава, когато prev_amount е 0 и какво като е отрицателен?

В описанието на клипа съм сложи бърза навигация до всяка подсума, а може да ползвате контрола на скоростта на плеъра (двойна или наполовина) да ускорити или забавите изпълнението. 

Всичкия код е достъпен в Github като съм добавил линк в описанието.

Благодаря за вниманието.


   



# Източници
* https://algorithmist.com/wiki/Min-Coin_change
* https://en.wikipedia.org/wiki/Optimal_substructure
* https://medium.com/@trykv/how-to-solve-minimum-coin-change-f96a758ccade



