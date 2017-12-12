import Prelude hiding (lookup)

-- Implement a binary search tree (4 points)
-- 2 extra points for a balanced tree
data BinaryTree k v = Nil | Node k v (BinaryTree k v) (BinaryTree k v) deriving Show

-- “Ord k =>” requires, that the elements of type k are comparable
-- Takes a key and a tree and returns Just value if the given key is present,
-- otherwise returns Nothing
lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup _ Nil    = Nothing
lookup k (Node k' v' l' r')
    | k > k'    = lookup k r'
    | k < k'    = lookup k l'
    | otherwise = Just v'

-- Takes a key, value and tree and returns a new tree with key/value pair inserted.
-- If the given key was already present, the value is updated in the new tree.
insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Nil  = (Node k v Nil Nil)
insert k v (Node k' v' l' r')
    | k > k'    = (Node k' v' l' (insert k v r'))
    | k < k'    = (Node k' v' (insert k v l') r')
    | otherwise = (Node k v l' r')

-- Returns a new tree without the given key
delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k Nil    = Nil
delete k (Node k' v' l' r')
    | k > k'    = (Node k' v' l' (delete k r'))
    | k < k'    = (Node k' v' (delete k l') r')
    | otherwise = (phd (Node k' v' l' r'))
         --phd means "put head down".
         where phd :: BinaryTree k v -> BinaryTree k v
               phd Nil                             = Nil
               phd (Node k v Nil r)                = r
               phd (Node k v (Node k' v' l' r') r) = (Node k' v' (phd (Node k v l' r')) r)
