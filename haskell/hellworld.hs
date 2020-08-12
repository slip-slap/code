import Data.Char
import Control.Monad

main = forever $ do
    putStr "give me some input: "
    l <- getLine
    putStrLn $ map toUpper l


{--
import Data.Char
    putStrLn "What's your first name?"
    firstName <- getLine
    putStrLn "What's your last name?"
    lastName <- getLine
    let bigFirstName = map toUpper firstName
        bigLastName = map toUpper lastName
    putStrLn $ "hey " ++ bigFirstName ++ " " ++ bigLastName ++ ", how are you?" 
--}
