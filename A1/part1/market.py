from concurrent import futures
import grpc
import shopping_pb2
import shopping_pb2_grpc

class ShoppingServicer(shopping_pb2_grpc.ShoppingServiceServicer):
    def __init__(self):
        self.sellers = {}  # uuid: address
        self.items = {}  # item_id: item
        self.next_item_id = 1
        self.wishlist = {}  # item_id: [buyer_address]
        self.item_ratings = {}  # item_id: [ratings]
        self.notifications = {}  # clientId: [Notification messages]

    def RegisterSeller(self, request, context):
        print(f"Seller join request from {request.address}, uuid = {request.uuid}")
        if request.uuid in self.sellers:
            return shopping_pb2.RegisterSellerResponse(success=False)
        self.sellers[request.uuid] = request.address
        return shopping_pb2.RegisterSellerResponse(success=True)

    def SellItem(self, request, context):
        print(f"Sell Item request from {request.seller_address}")
        item_id = str(self.next_item_id)
        self.next_item_id += 1
        self.items[item_id] = shopping_pb2.Item(
            id=item_id,
            name=request.name,
            category=request.category,
            description=request.description,
            price=request.price,
            quantity=request.quantity,
            rating=0,  # Initial rating
            seller_address=request.seller_address
        )
        return shopping_pb2.SellItemResponse(success=True, item_id=item_id)

    def UpdateItem(self, request, context):
        print(f"Update Item {request.item_id} request from {request.seller_address}")
        category_names = {
            shopping_pb2.Category.ELECTRONICS: "ELECTRONICS",
            shopping_pb2.Category.FASHION: "FASHION",
            shopping_pb2.Category.OTHERS: "OTHERS",
            shopping_pb2.Category.ANY: "ANY"
        }

        if request.item_id in self.items:
            item = self.items[request.item_id]
            item.price = request.new_price
            item.quantity = request.new_quantity
            self.items[request.item_id] = item
            category_name = category_names.get(item.category, "UNKNOWN")
            notification_message = f"The Following Item has been updated:\n\n" \
                                f"Item ID: {item.id}, Price: ${item.price}, Name: {item.name}, " \
                                f"Category: {category_name},\n" \
                                f"Description: {item.description},\n" \
                                f"Quantity Remaining: {item.quantity},\n" \
                                f"Rating: {item.rating} / 5  |  Seller: {item.seller_address}"

            # Notify all buyers who wishlisted this item
            if request.item_id in self.wishlist:
                for clientId in self.wishlist[request.item_id]:
                    self.add_notification(clientId, notification_message)

            return shopping_pb2.UpdateItemResponse(success=True)
        else:
            return shopping_pb2.UpdateItemResponse(success=False)

    def DeleteItem(self, request, context):
        print(f"Delete Item {request.item_id} request from {request.seller_address}")
        if request.item_id in self.items:
            del self.items[request.item_id]
            return shopping_pb2.DeleteItemResponse(success=True)
        else:
            return shopping_pb2.DeleteItemResponse(success=False)

    def DisplaySellerItems(self, request, context):
        print(f"Display Items request from {request.seller_address}")
        seller_items = [item for item in self.items.values() if item.seller_address == request.seller_address]
        return shopping_pb2.DisplaySellerItemsResponse(items=seller_items)

    def SearchItem(self, request, context):
        print(f"Search request for Item name: {request.name if request.name else '<empty>'}, Category: {request.category.name if request.category != shopping_pb2.Category.ANY else 'ANY'}.")
        filtered_items = [
            item for item in self.items.values()
            if (item.name == request.name or request.name == "") and
               (item.category == request.category or request.category == shopping_pb2.Category.ANY)
        ]
        return shopping_pb2.SearchItemResponse(items=filtered_items)

    def BuyItem(self, request, context):
        print(f"Buy request {request.quantity} of item {request.item_id}, from {request.buyer_address}")
        category_names = {
            shopping_pb2.Category.ELECTRONICS: "ELECTRONICS",
            shopping_pb2.Category.FASHION: "FASHION",
            shopping_pb2.Category.OTHERS: "OTHERS",
            shopping_pb2.Category.ANY: "ANY"
        }

        if request.item_id in self.items and self.items[request.item_id].quantity >= request.quantity:
            self.items[request.item_id].quantity -= request.quantity
            item = self.items[request.item_id]
            seller_client_id = item.seller_address  # Or use a mapping to find the seller's clientId
            category_name = category_names.get(item.category, "UNKNOWN")
            notification_message = f"The Following Item has been updated:\n\n" \
                                f"Item ID: {item.id}, Price: ${item.price}, Name: {item.name}, " \
                                f"Category: {category_name},\n" \
                                f"Description: {item.description},\n" \
                                f"Quantity Remaining: {item.quantity},\n" \
                                f"Rating: {item.rating} / 5  |  Seller: {item.seller_address}"

            # Notify the seller about the purchase
            self.add_notification(seller_client_id, notification_message)
            return shopping_pb2.BuyItemResponse(success=True)
        else:
            return shopping_pb2.BuyItemResponse(success=False)

    def AddToWishList(self, request, context):
        print(f"Wishlist request of item {request.item_id}, from {request.buyer_address}")
        if request.item_id in self.wishlist:
            self.wishlist[request.item_id].append(request.buyer_address)
        else:
            self.wishlist[request.item_id] = [request.buyer_address]
        return shopping_pb2.AddToWishListResponse(success=True)

    def RateItem(self, request, context):
        print(f"{request.buyer_address} rated item {request.item_id} with {request.rating} stars.")
        if request.item_id in self.item_ratings:
            self.item_ratings[request.item_id].append(request.rating)
        else:
            self.item_ratings[request.item_id] = [request.rating]
        # Update item rating
        self.items[request.item_id].rating = sum(self.item_ratings[request.item_id]) / len(self.item_ratings[request.item_id])
        return shopping_pb2.RateItemResponse(success=True)
    
    def NotifyClient(self, request, context):
        clientId = request.clientId
        notifications = self.notifications.get(clientId, [])
        #print(notifications)
         # Clear notifications after delivering
        self.notifications[clientId] = []
        return shopping_pb2.NotificationAck(message=notifications)

    # Utility method to add a notification
    def add_notification(self, clientId, message):
        if clientId not in self.notifications:
            self.notifications[clientId] = []
        self.notifications[clientId].append(message)

        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_pb2_grpc.add_ShoppingServiceServicer_to_server(ShoppingServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting server. Listening on port 50051.")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
