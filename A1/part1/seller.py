import grpc
import shopping_pb2
import shopping_pb2_grpc
import uuid

class SellerClient:
    def __init__(self, address):
        self.channel = grpc.insecure_channel(address)
        self.stub = shopping_pb2_grpc.ShoppingStub(self.channel)
        self.seller_uuid = str(uuid.uuid1())
        self.seller_address = "localhost:50051"  # Example seller address for notification server

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
            print(f"Item listed successfully with Item ID: {response.itemId}")
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
        response = self.stub.DisplaySellerItems(shopping_pb2.DisplaySellerItemsRequest(
            uuid=self.seller_uuid,
            seller_address=self.seller_address
        ))
        for item in response.items:
            print(f"""
–
Item ID: {item.id}, Name: {item.name}, Category: {item.category.name},
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

