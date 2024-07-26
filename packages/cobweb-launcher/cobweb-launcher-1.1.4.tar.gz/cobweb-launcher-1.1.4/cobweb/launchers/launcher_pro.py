import time
import threading

from cobweb.db import RedisDB
from cobweb.base import Seed, logger
from cobweb.launchers import Launcher
from cobweb.constant import DealModel, LogTemplate


class LauncherPro(Launcher):

    def __init__(self, task, project, custom_setting=None):
        super().__init__(task, project, custom_setting)
        self._todo = "{%s:%s}:todo" % (project, task)
        self._done = "{%s:%s}:done" % (project, task)
        self._fail = "{%s:%s}:fail" % (project, task)
        self._heartbeat = "heartbeat:%s_%s" % (project, task)
        self._reset_lock = "lock:reset:%s_%s" % (project, task)
        self._db = RedisDB()

        self._heartbeat_start_event = threading.Event()
        self._redis_queue_empty_event = threading.Event()

    @property
    def heartbeat(self):
        return self._db.exists(self._heartbeat)

    def _execute_heartbeat(self):
        while not self._stop.is_set():
            if self._heartbeat_start_event.is_set():
                self._db.setex(self._heartbeat, 3)
            time.sleep(2)

    def _reset(self):
        """
        检查过期种子，重新添加到redis缓存中
        """
        init = True
        while not self._pause.is_set():
            reset_wait_seconds = 30
            start_reset_time = int(time.time())
            if self._db.lock(self._reset_lock, t=120):
                if not self.heartbeat:
                    self._heartbeat_start_event.set()

                _min = -int(time.time()) + self._seed_reset_seconds \
                    if self.heartbeat or not init else "-inf"

                self._db.members(self._todo, 0, _min=_min, _max="(0")
                self._db.delete(self._reset_lock)

                ttl = 120 - int(time.time()) + start_reset_time
                reset_wait_seconds = max(ttl, 1)
            time.sleep(reset_wait_seconds)
            init = False

    def _scheduler(self):
        """
        调度任务，获取redis队列种子，同时添加到doing字典中
        """
        if self.start_seeds:
            self.__LAUNCHER_QUEUE__['todo'].push(self.start_seeds)
        while not self._pause.is_set():
            if not self._db.zcount(self._todo, 0, "(1000"):
                time.sleep(self._scheduler_wait_seconds)
                continue
            if self.__LAUNCHER_QUEUE__['todo'].length >= self._todo_queue_size:
                time.sleep(self._todo_queue_full_wait_seconds)
                continue
            members = self._db.members(
                self._todo, int(time.time()),
                count=self._todo_queue_size,
                _min=0, _max="(1000"
            )
            for member, priority in members:
                seed = Seed(member, priority=priority)
                self.__LAUNCHER_QUEUE__['todo'].push(seed)
                self.__DOING__[seed.to_string] = seed.params.priority

    def _insert(self):
        """
        添加新种子到redis队列中
        """
        while not self._pause.is_set():
            seeds = {}
            status = self.__LAUNCHER_QUEUE__['new'].length < self._new_queue_max_size
            for _ in range(self._new_queue_max_size):
                seed = self.__LAUNCHER_QUEUE__['new'].pop()
                if not seed:
                    break
                seeds[seed.to_string] = seed.params.priority
            if seeds:
                self._db.zadd(self._todo, seeds, nx=True)
            if status:
                time.sleep(self._new_queue_wait_seconds)

    def _refresh(self):
        """
        刷新doing种子过期时间，防止reset重新消费
        """
        while not self._pause.is_set():
            if self.__DOING__:
                refresh_time = int(time.time())
                seeds = {k:-refresh_time - v / 1000 for k, v in self.__DOING__.items()}
                self._db.zadd(self._todo, item=seeds, xx=True)
            time.sleep(30)

    def _delete(self):
        """
        删除队列种子，根据状态添加至成功或失败队列，移除doing字典种子索引
        """
        while not self._pause.is_set():
            seeds, s_seeds, f_seeds = [], [], []
            status = self.__LAUNCHER_QUEUE__['done'].length < self._done_queue_max_size

            for _ in range(self._done_queue_max_size):
                seed = self.__LAUNCHER_QUEUE__['done'].pop()
                if not seed:
                    break
                if seed.params.identifier == DealModel.fail:
                    f_seeds.append(seed.to_string)
                elif self._done_model == 1:
                    s_seeds.append(seed.to_string)
                else:
                    seeds.append(seed.to_string)
            if seeds:
                self._db.zrem(self._todo, *seeds)
            if s_seeds:
                self._db.done([self._todo, self._done], *s_seeds)
            if f_seeds:
                self._db.done([self._todo, self._fail], *f_seeds)

            self._remove_doing_seeds(seeds)

            if status:
                time.sleep(self._done_queue_wait_seconds)

    def _polling(self):
        check_emtpy_times = 0
        while not self._stop.is_set():
            queue_not_empty_count = 0
            pooling_wait_seconds = 30
            if not self._db.zcard(self._todo):
                for q in self.__LAUNCHER_QUEUE__.values():
                    if q.length != 0:
                        queue_not_empty_count += 1
                if self._pause.is_set():
                    self._pause.clear()
                    self._execute()
                elif queue_not_empty_count == 0:
                    pooling_wait_seconds = 3
                    check_emtpy_times += 1
                else:
                    check_emtpy_times = 0
                if check_emtpy_times > 2:
                    check_emtpy_times = 0
                    self.__DOING__ = {}
                    self._pause.set()
            if not self._pause.is_set():
                logger.info(LogTemplate.launcher_pro_polling.format(
                    task=self.task,
                    doing_len=len(self.__DOING__.keys()),
                    todo_len=self.__LAUNCHER_QUEUE__['todo'].length,
                    done_len=self.__LAUNCHER_QUEUE__['done'].length,
                    redis_seed_count=self._db.zcount(self._todo, "-inf", "+inf"),
                    redis_todo_len=self._db.zcount(self._todo, 0, "(1000"),
                    redis_doing_len=self._db.zcount(self._todo, "-inf", "(0"),
                    upload_len=self._upload_queue.length
                ))
            time.sleep(pooling_wait_seconds)
