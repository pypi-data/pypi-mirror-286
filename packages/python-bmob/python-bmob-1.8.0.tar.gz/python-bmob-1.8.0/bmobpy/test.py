from bmob import *

b = Bmob('','')
query = BmobQuery().addWhereGreaterThan('updatedAt',BmobDate('2024-07-24 14:23:49')).addWhereEqualTo('role','user')
rs = b.findObjects('ai_log',where=query,limit=20)

for r in rs:
    print(r)
    print('')


# {"$and":
#     [
#         {"createdAt":{"$gte":{"__type": "Date", "iso": "2014-07-15 00:00:00"}}},
#         {"createdAt":{"$lte":{"__type": "Date", "iso": "2014-07-15 23:59:59"}}}
#     ]
# }
