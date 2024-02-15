# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: shopping.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eshopping.proto\x12\x08shopping\"G\n\x11SearchItemRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12$\n\x08\x63\x61tegory\x18\x02 \x01(\x0e\x32\x12.shopping.Category\"\xa4\x01\n\x04Item\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12$\n\x08\x63\x61tegory\x18\x03 \x01(\x0e\x32\x12.shopping.Category\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\r\n\x05price\x18\x05 \x01(\x02\x12\x10\n\x08quantity\x18\x06 \x01(\x05\x12\x0e\n\x06rating\x18\x07 \x01(\x02\x12\x16\n\x0eseller_address\x18\x08 \x01(\t\"3\n\x12SearchItemResponse\x12\x1d\n\x05items\x18\x01 \x03(\x0b\x32\x0e.shopping.Item\"J\n\x0e\x42uyItemRequest\x12\x0f\n\x07item_id\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\x12\x15\n\rbuyer_address\x18\x03 \x01(\t\"\"\n\x0f\x42uyItemResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\">\n\x14\x41\x64\x64ToWishListRequest\x12\x0f\n\x07item_id\x18\x01 \x01(\t\x12\x15\n\rbuyer_address\x18\x02 \x01(\t\"(\n\x15\x41\x64\x64ToWishListResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"I\n\x0fRateItemRequest\x12\x0f\n\x07item_id\x18\x01 \x01(\t\x12\x0e\n\x06rating\x18\x02 \x01(\x05\x12\x15\n\rbuyer_address\x18\x03 \x01(\t\"#\n\x10RateItemResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\'\n\x13NotificationRequest\x12\x10\n\x08\x63lientId\x18\x01 \x01(\t\"\"\n\x0fNotificationAck\x12\x0f\n\x07message\x18\x01 \x03(\t\"6\n\x15RegisterSellerRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\")\n\x16RegisterSellerResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\xa1\x01\n\x0fSellItemRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12$\n\x08\x63\x61tegory\x18\x03 \x01(\x0e\x32\x12.shopping.Category\x12\x10\n\x08quantity\x18\x04 \x01(\x05\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\r\n\x05price\x18\x06 \x01(\x02\x12\x16\n\x0eseller_address\x18\x07 \x01(\t\"4\n\x10SellItemResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07item_id\x18\x02 \x01(\t\"s\n\x11UpdateItemRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0f\n\x07item_id\x18\x02 \x01(\t\x12\x11\n\tnew_price\x18\x03 \x01(\x02\x12\x14\n\x0cnew_quantity\x18\x04 \x01(\x05\x12\x16\n\x0eseller_address\x18\x05 \x01(\t\"%\n\x12UpdateItemResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"J\n\x11\x44\x65leteItemRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0f\n\x07item_id\x18\x02 \x01(\t\x12\x16\n\x0eseller_address\x18\x03 \x01(\t\"%\n\x12\x44\x65leteItemResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"A\n\x19\x44isplaySellerItemsRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x16\n\x0eseller_address\x18\x02 \x01(\t\";\n\x1a\x44isplaySellerItemsResponse\x12\x1d\n\x05items\x18\x01 \x03(\x0b\x32\x0e.shopping.Item*=\n\x08\x43\x61tegory\x12\x0f\n\x0b\x45LECTRONICS\x10\x00\x12\x0b\n\x07\x46\x41SHION\x10\x01\x12\n\n\x06OTHERS\x10\x02\x12\x07\n\x03\x41NY\x10\x03\x32\x84\x06\n\x0fShoppingService\x12G\n\nSearchItem\x12\x1b.shopping.SearchItemRequest\x1a\x1c.shopping.SearchItemResponse\x12>\n\x07\x42uyItem\x12\x18.shopping.BuyItemRequest\x1a\x19.shopping.BuyItemResponse\x12P\n\rAddToWishList\x12\x1e.shopping.AddToWishListRequest\x1a\x1f.shopping.AddToWishListResponse\x12\x41\n\x08RateItem\x12\x19.shopping.RateItemRequest\x1a\x1a.shopping.RateItemResponse\x12H\n\x0cNotifyClient\x12\x1d.shopping.NotificationRequest\x1a\x19.shopping.NotificationAck\x12S\n\x0eRegisterSeller\x12\x1f.shopping.RegisterSellerRequest\x1a .shopping.RegisterSellerResponse\x12\x41\n\x08SellItem\x12\x19.shopping.SellItemRequest\x1a\x1a.shopping.SellItemResponse\x12G\n\nUpdateItem\x12\x1b.shopping.UpdateItemRequest\x1a\x1c.shopping.UpdateItemResponse\x12G\n\nDeleteItem\x12\x1b.shopping.DeleteItemRequest\x1a\x1c.shopping.DeleteItemResponse\x12_\n\x12\x44isplaySellerItems\x12#.shopping.DisplaySellerItemsRequest\x1a$.shopping.DisplaySellerItemsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'shopping_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CATEGORY']._serialized_start=1444
  _globals['_CATEGORY']._serialized_end=1505
  _globals['_SEARCHITEMREQUEST']._serialized_start=28
  _globals['_SEARCHITEMREQUEST']._serialized_end=99
  _globals['_ITEM']._serialized_start=102
  _globals['_ITEM']._serialized_end=266
  _globals['_SEARCHITEMRESPONSE']._serialized_start=268
  _globals['_SEARCHITEMRESPONSE']._serialized_end=319
  _globals['_BUYITEMREQUEST']._serialized_start=321
  _globals['_BUYITEMREQUEST']._serialized_end=395
  _globals['_BUYITEMRESPONSE']._serialized_start=397
  _globals['_BUYITEMRESPONSE']._serialized_end=431
  _globals['_ADDTOWISHLISTREQUEST']._serialized_start=433
  _globals['_ADDTOWISHLISTREQUEST']._serialized_end=495
  _globals['_ADDTOWISHLISTRESPONSE']._serialized_start=497
  _globals['_ADDTOWISHLISTRESPONSE']._serialized_end=537
  _globals['_RATEITEMREQUEST']._serialized_start=539
  _globals['_RATEITEMREQUEST']._serialized_end=612
  _globals['_RATEITEMRESPONSE']._serialized_start=614
  _globals['_RATEITEMRESPONSE']._serialized_end=649
  _globals['_NOTIFICATIONREQUEST']._serialized_start=651
  _globals['_NOTIFICATIONREQUEST']._serialized_end=690
  _globals['_NOTIFICATIONACK']._serialized_start=692
  _globals['_NOTIFICATIONACK']._serialized_end=726
  _globals['_REGISTERSELLERREQUEST']._serialized_start=728
  _globals['_REGISTERSELLERREQUEST']._serialized_end=782
  _globals['_REGISTERSELLERRESPONSE']._serialized_start=784
  _globals['_REGISTERSELLERRESPONSE']._serialized_end=825
  _globals['_SELLITEMREQUEST']._serialized_start=828
  _globals['_SELLITEMREQUEST']._serialized_end=989
  _globals['_SELLITEMRESPONSE']._serialized_start=991
  _globals['_SELLITEMRESPONSE']._serialized_end=1043
  _globals['_UPDATEITEMREQUEST']._serialized_start=1045
  _globals['_UPDATEITEMREQUEST']._serialized_end=1160
  _globals['_UPDATEITEMRESPONSE']._serialized_start=1162
  _globals['_UPDATEITEMRESPONSE']._serialized_end=1199
  _globals['_DELETEITEMREQUEST']._serialized_start=1201
  _globals['_DELETEITEMREQUEST']._serialized_end=1275
  _globals['_DELETEITEMRESPONSE']._serialized_start=1277
  _globals['_DELETEITEMRESPONSE']._serialized_end=1314
  _globals['_DISPLAYSELLERITEMSREQUEST']._serialized_start=1316
  _globals['_DISPLAYSELLERITEMSREQUEST']._serialized_end=1381
  _globals['_DISPLAYSELLERITEMSRESPONSE']._serialized_start=1383
  _globals['_DISPLAYSELLERITEMSRESPONSE']._serialized_end=1442
  _globals['_SHOPPINGSERVICE']._serialized_start=1508
  _globals['_SHOPPINGSERVICE']._serialized_end=2280
# @@protoc_insertion_point(module_scope)
