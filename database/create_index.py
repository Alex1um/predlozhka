from database.database import database as r
from redis.commands.search.field import NumericField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

channel_schema = {
    TextField("$.name", as_name="name"),
    NumericField("$.admin_id", as_name="admin_id"),
}

rs = r.ft("idx:channels")
rs.create_index(
    channel_schema,
    definition=IndexDefinition(
        prefix=["channels:"],
        index_type=IndexType.JSON,
    ),
)

user_schema = {
    NumericField("$.chat_id", as_name="chat_id"),
}

rs = r.ft("idx:users")
rs.create_index(
    user_schema,
    definition=IndexDefinition(
        prefix=["users:"],
        index_type=IndexType.JSON,
    ),
)
