import Prelude hiding (lookup)

-- Implement a binary search tree (4 points)
-- 2 extra points for a balanced tree
data BinaryTree k v = Nil | Node k v (BinaryTree k v) (BinaryTree k v) deriving Show

-- “Ord k =>” requires, that the elements of type k are comparable
-- Takes a key and a tree and returns Just value if the given key is present,
-- otherwise returns Nothing
lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup _ Nil = Nothing
lookup k (Node key v left right) | k == key = Just v
                                 | k > key = lookup k right
                                 | k < key = lookup k left

-- Takes a key, value and tree and returns a new tree with key/value pair inserted.
-- If the given key was already present, the value is updated in the new tree.
insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v (Node key _ left right) | k == key = (Node k v left right)
                                   | k > key = insert k v right
                                   | k < key = insert k v left

-- Returns a new tree without the given key
delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k Nil = Nil
delete k (Node key _ Nil right) | k == key = right
                                | otherwise = delete k right
delete k (Node key  v 
         (Node lkey lv lleft lright) right) | k == key =  (Node lkey lv 
                                              (delete key (Node key   v lleft lright)) right)
                                            | k > key = delete k right
                                            | k < key = delete k (Node lkey lv lleft lright)
