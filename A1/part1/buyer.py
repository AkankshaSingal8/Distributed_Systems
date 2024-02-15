import grpc
import shopping_pb2
import shopping_pb2_grpc
import threading
import time
import threading
import time
import uuid


def listen_for_notifications(stub, buyer_address):
    def notification_listener():
        while True:  # Outer loop to reconnect in case of disconnection
            try:
                response = stub.NotifyClient(shopping_pb2.NotificationRequest(clientId=buyer_address))
                for notification in response.message:
                    print(notification)
                # If the server closes the connection, the for-loop will exit.
            except grpc.RpcError as e:
                  time.sleep(10)# Wait before attempting to reconnect

            time.sleep(10) 
    # Start the listener thread
    listener_thread = threading.Thread(target=notification_listener, daemon=True)
    listener_thread.start()


def search_item(stub):
    name = input("Enter item name (leave blank for all items): ")
    category = input("Enter category (ELECTRONICS, FASHION, OTHERS, ANY): ").upper()
    category_names = {
            shopping_pb2.Category.ELECTRONICS: "ELECTRONICS",
            shopping_pb2.Category.FASHION: "FASHION",
            shopping_pb2.Category.OTHERS: "OTHERS",
            shopping_pb2.Category.ANY: "ANY"
    }

    try:
        category_enum = getattr(shopping_pb2.Category, category)
    except AttributeError:
        category_enum = shopping_pb2.ANY
    
    response = stub.SearchItem(shopping_pb2.SearchItemRequest(name=name, category=category_enum))
    for item in response.items:
        category_name = category_names.get(item.category, "UNKNOWN")
        print(f"""
–
Item ID: {item.id}, Price: ${item.price}, Name: {item.name}, Category: {category_name},
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


buyer_address = "localhost:50053"


with grpc.insecure_channel('localhost:50051') as channel:  # Assume Market is on localhost:50051
    stub = shopping_pb2_grpc.ShoppingServiceStub(channel)
    listen_for_notifications(stub, buyer_address)
    
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

