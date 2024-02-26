# import logging
# from typing import Literal
#
# from aioredis import Redis as AsyncRedis
# from redis import Redis as SyncRedis
#
# from project.settings import (
#     REDIS_HOST,
#     REDIS_PASSWORD,
#     REDIS_PORT,
#     REDIS_USERNAME,
# )
#
# dev_logger = logging.getLogger("dev")
#
# __all__ = (
#     "SyncRedisConnector",
#     "AsyncRedisConnector",
# )
#
# # Redis databases and what they store:
# # 0 - Use Taskiq. Stores messages. Don`t use.
# # 1 - Use Taskiq. Stores results. Don`t use.
# # 2 - Cache.
# # ...
# # 10 - Only for testing.
# # 11 - Stores hot client constant.
# allowed_numbers_of_databases = Literal[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
#
#
# class SyncRedisConnector:
#     def __init__(self, db: allowed_numbers_of_databases):
#         dev_logger.debug(f"Attempt to sync connect to Redis database #{db}.")
#         dev_logger.debug(f"Redis host: {REDIS_HOST}, Redis port: {REDIS_PORT}")
#         self.conn = SyncRedis(
#             host=REDIS_HOST,
#             port=int(REDIS_PORT),
#             db=db,
#             decode_responses=True,
#         )
#
#     def __enter__(self) -> SyncRedis:
#         return self.conn
#
#     def __exit__(self, exc_type, exc_val, exc_tb) -> None:
#         self.conn.close()
#
#
# class AsyncRedisConnector:
#     def __init__(self, db: allowed_numbers_of_databases):
#         dev_logger.debug(f"Attempt async connect to Redis database #{db}.")
#         dev_logger.debug(f"Redis host: {REDIS_HOST}, Redis port: {REDIS_PORT}")
#         self.coro_conn = AsyncRedis.from_url(
#             url=f"redis://{REDIS_HOST}:{REDIS_PORT}",
#             db=db,
#             decode_responses=True,
#         )
#
#     async def __aenter__(self) -> AsyncRedis:
#         return await self.coro_conn
#
#     async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
#         await self.coro_conn.close()
