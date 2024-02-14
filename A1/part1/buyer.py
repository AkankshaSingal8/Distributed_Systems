import grpc
import shopping_pb2
import shopping_pb2_grpc

def search_item(stub):
    name = input("Enter item name (leave blank for all items): ")
    category = input("Enter category (ELECTRONICS, FASHION, OTHERS, ANY): ").upper()
    try:
        category_enum = getattr(shopping_pb2.Category, category)
    except AttributeError:
        category_enum = shopping_pb2.ANY
    
    response = stub.SearchItem(shopping_pb2.SearchItemRequest(name=name, category=category_enum))
    for item in response.items:
        print(f"""
–
Item ID: {item.id}, Price: ${item.price}, Name: {item.name}, Category: {item.category.name},
Description: {item.description}.
Quantity Remaining: {item.quantity}
Rating: {item.rating} / 5 | Seller: {item.seller_address}
–
""")

def buy_item(stub, buyer_address):
    item_id = input("Enter item ID to buy: ")
    quantity = int(input("Enter quantity: "))
    response = stub.BuyItem(shopping_pb2.BuyItemRequest(item_id=item_id, quantity=quantity, buyer_address=buyer_address))
    print("SUCCESS" if response.success else "FAIL")

def add_to_wishlist(stub, buyer_address):
    item_id = input("Enter item ID to add to wishlist: ")
    response = stub.AddToWishList(shopping_pb2.AddToWishListRequest(item_id=item_id, buyer_address=buyer_address))
    print("SUCCESS" if response.success else "FAIL")

def rate_item(stub, buyer_address):
    item_id = input("Enter item ID to rate: ")
    rating = int(input("Rate the item (1-5): "))
    response = stub.RateItem(shopping_pb2.RateItemRequest(item_id=item_id, rating=rating, buyer_address=buyer_address))
    print("SUCCESS" if response.success else "FAIL")


buyer_address = "localhost:50052"

with grpc.insecure_channel('localhost:50051') as channel:  # Assume Market is on localhost:50051
    stub = shopping_pb2_grpc.ShoppingServiceStub(channel)
    
    actions = {
        "1": search_item,
        "2": lambda stub: buy_item(stub, buyer_address),
        "3": lambda stub: add_to_wishlist(stub, buyer_address),
        "4": lambda stub: rate_item(stub, buyer_address),
    }

    while True:
        print("""
Choose an action:
1. Search for items
2. Buy an item
3. Add an item to wishlist
4. Rate an item
5. Exit
""")
        choice = input("Enter your choice: ")
        if choice == "5":
            break
        action = actions.get(choice)
        if action:
            action(stub)
        else:
            print("Invalid choice.")

