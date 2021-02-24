SELECT Item.ItemID
FROM Item
WHERE Item.Currently = (SELECT MAX(Currently) from Item);
