import logging
logger = logging.getLogger('Redis')

import os
from typing import Any, Dict, Iterable, List, Tuple

import redis

HOST = os.getenv('REDIS_HOST')
if not HOST:
	raise RuntimeError('missing "REDIS_HOST" env var')

PORT_RAW = os.getenv('REDIS_PORT')
if not PORT_RAW:
	raise RuntimeError('missing "REDIS_PORT" env var')

DB_RAW = os.getenv('REDIS_DB')
if not DB_RAW:
	raise RuntimeError('missing "REDIS_DB" env var')

PORT = int(PORT_RAW)
DB = int(DB_RAW)

class RedisClient:
	def __init__(self) -> None:
		self._client = redis.Redis(
			host=HOST,
			port=PORT,
			db=DB,
			decode_responses=True,
			socket_timeout=5,
			socket_connect_timeout=5,
			health_check_interval=30,
		)

	# --------------- Cache helpers ---------------
	def get(self, key: str) -> str | None:
		return self._client.get(key)

	def set(self, key: str, value: str, ex_seconds: int | None = None) -> bool:
		return bool(self._client.set(name=key, value=value, ex=ex_seconds))

	def incrby(self, key: str, amount: int = 1) -> int:
		return int(self._client.incrby(name=key, amount=amount))

	# --------------- Stream helpers ---------------
	def create_consumer_group(self, stream: str, group: str) -> None:
		try:
			self._client.xgroup_create(name=stream, groupname=group, id='$', mkstream=True)
			logger.info(f'created consumer group {group} for stream {stream}')
		
		except redis.ResponseError as e:
			if 'BUSYGROUP' in str(e):
				return
			
			raise

	def add_to_stream(self, stream: str, fields: Dict[str, Any]) -> str:
		return str(self._client.xadd(name=stream, fields=fields))

	def read_group(
		self,
		stream: str,
		group: str,
		consumer: str,
		count: int = 10,
		block_ms: int = 5000,
	) -> List[Tuple[str, Dict[str, str]]]:
		messages = self._client.xreadgroup(
			groupname=group,
			consumername=consumer,
			streams={stream: '>'},
			count=count,
			block=block_ms,
		)

		if not messages:
			return []
		
		_, items = messages[0]
		return [(mid, {k: v for k, v in data.items()}) for (mid, data) in items]

	def ack(self, stream: str, group: str, message_id: str) -> int:
		return int(self._client.xack(name=stream, groupname=group, id=message_id))

	def pending(self, stream: str, group: str, idle_ms: int, count: int = 50) -> List[str]:
		# Get a range of pending messages older than idle_ms
		try:
			pendings = self._client.xpending_range(name=stream, groupname=group, min_idle_time=idle_ms, start='-', end='+', count=count)
		
		except AttributeError:
			# Fallback for clients without xpending_range
			info = self._client.xpending(name=stream, groupname=group)
			if not info or info.get('pending') == 0:
				return []
			
			pendings = []
		
		return [p['message_id'] if isinstance(p, dict) else p[0] for p in pendings]

	def claim(self, stream: str, group: str, consumer: str, min_idle_ms: int, message_ids: Iterable[str]) -> List[str]:
		if not message_ids:
			return []
		
		try:
			claimed = self._client.xclaim(name=stream, groupname=group, consumername=consumer, min_idle_time=min_idle_ms, message_ids=list(message_ids))
		except redis.ResponseError:
			return []
		
		return [mid for (mid, _data) in claimed]


# Singleton instance
_instance: RedisClient | None = None

def new_client() -> RedisClient:
	global _instance
	if _instance is None:
		_instance = RedisClient()
	
	return _instance
