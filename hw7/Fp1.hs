-- 1. head' возвращает первый элемент непустого списка (0,5 балла)
head' :: [a] -> a
head' (a:_) = a
-- 2. tail' возвращает список без первого элемента, для пустого - пустой (0,5)
tail' :: [a] -> [a]
tail' [] = []
tail' (_:as) = as
-- 3. take' возвращает первые n >= 0 элементов исходного списка (0,5)
take' :: Int -> [a] -> [a]
take' 0 _ = []
take' _ [] = []
take' n (a:as) = a:(take' (n - 1) as)
-- 4. drop' возвращает список без первых n >= 0 элементов; если n больше длины
-- списка, то пустой список. (0,5)
drop' :: Int -> [a] -> [a]
drop' 0 a = a
drop' _ [] = []
drop' n (a:as) = drop' (n - 1) as
-- 5. filter' возвращает список из элементов, для которых f возвращает True (0,5)
filter' :: (a -> Bool) -> [a] -> [a]
filter' _ [] = []
filter' f (a:as) | f a = a:(filter'  f as)
                 | otherwise = filter' f as 
-- 6. foldl' последовательно применяет функцию f к элементу списка l и значению,
-- полученному на предыдущем шаге, начальное значение z (0,5)
-- foldl' (+) 0 [1, 2, 3] == (((0 + 1) + 2) + 3)
-- foldl' (*) 4 [] == 4
foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' _ z [] = z
foldl' f z (l:ls) = foldl' f (f z l) ls
-- 7. concat' принимает на вход два списка и возвращает их конкатенацию (0,5)
-- concat' [1,2] [3] == [1,2,3]
concat' :: [a] -> [a] -> [a]
concat' [] b = b
concat' (a:as) b = a:concat' as b
-- 8. quickSort' возвращает его отсортированный список (0,5)
-- quickSort' должен быть реализован через алгоритм QuickSort
-- (выбор pivot может быть любым)
quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' (a:as) = concat' (quickSort' (filter' (a >) (a:as)))
                              $ concat' (filter' (a ==) (a:as))
                              $ quickSort' (filter' (a <) (a:as))
