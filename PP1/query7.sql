SELECT COUNT(*)
FROM (SELECT COUNT(DISTINCT Category.Category) 
    FROM Category, Bid
    WHERE Bid.Amount > 100 AND Bid.ItemID = Category.ItemID
    GROUP BY Category.Category);
