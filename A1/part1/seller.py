import grpc
import shopping_pb2
import shopping_pb2_grpc
import uuid
import threading
import time

class SellerClient:
    def __init__(self, address):
        self.channel = grpc.insecure_channel(address)
        self.stub = shopping_pb2_grpc.ShoppingServiceStub(self.channel)
        self.seller_uuid = str(uuid.uuid1())
        self.seller_address = "localhost:50052"  # Example seller address for notification server
        self.listen_for_notifications()

    def listen_for_notifications(self):
        def notification_listener():
            while True:  # Outer loop to reconnect in case of disconnection
                try:
                    response = self.stub.NotifyClient(shopping_pb2.NotificationRequest(clientId=self.seller_address))
                    for notification in response.message:
                        print(notification)
                    # If the server closes the connection, the for-loop will exit.
                except:
                    time.sleep(10)  # Wait before attempting to reconnect

                time.sleep(10)  # Wait before attempting to reconnect
        # Start the listener thread
        listener_thread = threading.Thread(target=notification_listener, daemon=True)
        listener_thread.start()

    def register_seller(self):
        response = self.stub.RegisterSeller(shopping_pb2.RegisterSellerRequest(
            uuid=self.seller_uuid, address=self.seller_address))
        print("Registration:", "SUCCESS" if response.success else "FAIL")

    def sell_item(self):
        name = input("Enter product name: ")
        category = input("Enter category (ELECTRONICS, FASHION, OTHERS): ").upper()
        quantity = int(input("Enter quantity: "))
        description = input("Enter description: ")
        price = float(input("Enter price per unit: "))
        response = self.stub.SellItem(shopping_pb2.SellItemRequest(
            uuid=self.seller_uuid,
            name=name,
            category=getattr(shopping_pb2.Category, category, shopping_pb2.OTHERS),
            quantity=quantity,
            description=description,
            price=price,
            seller_address=self.seller_address
        ))
        if response.success:
            print(f"Item listed successfully with Item ID: {response.item_id}")
        else:
            print("Failed to list item.")

    def update_item(self):
        item_id = input("Enter Item ID to update: ")
        price = float(input("Enter new price: "))
        quantity = int(input("Enter new quantity: "))
        response = self.stub.UpdateItem(shopping_pb2.UpdateItemRequest(
            uuid=self.seller_uuid,
            item_id=item_id,
            new_price=price,
            new_quantity=quantity,
            seller_address=self.seller_address
        ))
        print("Update Item:", "SUCCESS" if response.success else "FAIL")

    def delete_item(self):
        item_id = input("Enter Item ID to delete: ")
        response = self.stub.DeleteItem(shopping_pb2.DeleteItemRequest(
            uuid=self.seller_uuid,
            item_id=item_id,
            seller_address=self.seller_address
        ))
        print("Delete Item:", "SUCCESS" if response.success else "FAIL")

    def display_items(self):
        # Mapping of category enums to their string representations
        category_names = {
            shopping_pb2.Category.ELECTRONICS: "ELECTRONICS",
            shopping_pb2.Category.FASHION: "FASHION",
            shopping_pb2.Category.OTHERS: "OTHERS",
            shopping_pb2.Category.ANY: "ANY"
        }

        response = self.stub.DisplaySellerItems(shopping_pb2.DisplaySellerItemsRequest(
            uuid=self.seller_uuid,
            seller_address=self.seller_address
        ))
        for item in response.items:
            # Translate the category number to its name
            category_name = category_names.get(item.category, "UNKNOWN")

            print(f"""
    –
            Item ID: {item.id}, Name: {item.name}, Category: {category_name},
            Description: {item.description}, Quantity Remaining: {item.quantity},
            Price: ${item.price}, Rating: {item.rating} / 5
    –
            """)



seller_client = SellerClient('localhost:50051')  # Market server address
seller_client.register_seller()

actions = {
    "1": seller_client.sell_item,
    "2": seller_client.update_item,
    "3": seller_client.delete_item,
    "4": seller_client.display_items,
}

while True:
    print("""
Choose an action:
1. Sell an item
2. Update an item
3. Delete an item
4. Display all items
5. Exit
""")
    choice = input("Enter your choice: ")
    if choice == "5":
        break
    action = actions.get(choice)
    if action:
        action()
    else:
        print("Invalid choice.")

