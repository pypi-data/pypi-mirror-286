#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from abc import ABC, abstractmethod
import asyncio
import json
import os
import time
from typing import Any, Callable, Dict, Generic, Optional, Tuple, Type, TypeVar, Union

import aiofiles
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor

from ngcbpc.environ import NGC_CLI_PROGRESS_UPDATE_FREQUENCY
from ngcbpc.errors import NgcException
from ngcbpc.transfer.utils import (
    bitmask_clear_bit,
    bitmask_is_bit_set,
    bitmask_set_bit_in_size,
)

# contractral constant, cannot be modified without agreement
PARTITION_SIZE = 500000000

# This line instruments aiohttp client sessions and requests, enabling tracing functionality.
# It adds default trace configuration options to all aiohttp requests
AioHttpClientInstrumentor().instrument()

# This line instruments all asyncio functions, enabling tracing without the need to pass a tracer explicitly.
# In asyncio workers, where different contexts may exist for the overall execution and individual worker tasks,
# this instrumentation ensures that tracing captures and respects the distinct contexts of each worker's execution.
AsyncioInstrumentor().instrument()

NodeT = TypeVar("NodeT", bound="BaseFileNode")


class AsyncTransferProgress:
    """Tracks the state of a file during async transfer.

    Track overall transfer progress for a transfer, providing safe async updates and callback
    at a specified maximum update rate.
    """

    def __init__(
        self,
        completed_bytes: int = 0,
        failed_bytes: int = 0,
        total_bytes: int = 0,
        completed_count: int = 0,
        failed_count: int = 0,
        total_count: int = 0,
        callback_func: Optional[  # pylint: disable=unsubscriptable-object
            Callable[[int, int, int, int, int, int], Any]
        ] = None,
        update_rate=NGC_CLI_PROGRESS_UPDATE_FREQUENCY,
    ):
        """Initialize the AsyncTransferProgress instance.

        Args:
            completed_bytes (int): The number of completed bytes.
            failed_bytes (int): The number of failed bytes.
            total_bytes (int): The total number of bytes.
            completed_count (int): The number of completed items.
            failed_count (int): The number of failed items.
            total_count (int): The total number of items.
            callback_func (Optional[Callable[[int, int, int, int, int, int], Any]]):
                A callback function that accepts six integers representing
                completed_bytes, failed_bytes, total_bytes, completed_count,
                failed_count, and total_count respectively. If provided,
                this function will be called to report progress.
                If set to None, progress updates will not be reported.
            update_rate (float): The maximum update rate for the callback function,
                in seconds. Progress updates will be reported at most once per
                this duration. Ignored if callback_func is None.

        """
        self.lock = asyncio.Lock()
        self.completed_bytes = completed_bytes
        self.failed_bytes = failed_bytes
        self.total_bytes = total_bytes
        self.completed_count = completed_count
        self.failed_count = failed_count
        self.total_count = total_count
        self.callback_func = callback_func

        self.update_rate = update_rate if callback_func else -1
        self.next_update = time.time() + update_rate if callback_func else -1

    async def debounced_update_progress(self):
        """Call the update progress callback function if the specified update rate interval has passed.

        'callback_func' is a user provided function with limited capability during lots of concurrent updates.
        Be sure to call update_progress at the end to finalize progress update.
        """
        now = time.time()  # tiny bit less expensive than lock check, thus do it first
        if self.callback_func and now > self.next_update and (not self.lock.locked()):
            async with self.lock:
                self.next_update = now + self.update_rate
                self.update_progress()

    def update_progress(self):
        """Call the update progress callback function with the current progress metrics."""
        if self.callback_func:
            self.callback_func(
                self.completed_bytes,
                self.failed_bytes,
                self.total_bytes,
                self.completed_count,
                self.failed_count,
                self.total_count,
            )

    async def advance(self, size_in_bytes: int, count: int):
        """Advance the progress by adding completed bytes and item count.

        use negatives to undo
        """
        async with self.lock:
            self.completed_bytes += size_in_bytes
            self.completed_count += count
        await self.debounced_update_progress()

    async def fail(self, size_in_bytes: int, count: int):
        """Update the progress by adding failed bytes and item count.

        use negatives to undo
        """
        async with self.lock:
            self.failed_bytes += size_in_bytes
            self.failed_count += count
        await self.debounced_update_progress()

    def read_progress(self):
        """Read the current progress metrics."""
        return (
            self.completed_bytes,
            self.failed_bytes,
            self.total_bytes,
            self.completed_count,
            self.failed_count,
            self.total_count,
        )


class BaseFileNode:  # noqa: D101
    def __init__(
        self,
        file_path: str = "",
        size: int = -1,
        ftime: float = -1.0,
        bitmask: int = -1,
    ):
        """This base file node object tracks the state of a file during transfer.

        FileNode-level asynchronous access should be handled in child classes.
        Read operations typically do not require locking, while write operations usually do.
        Users can implement their own logic for bitmask manipulation if needed.

        Args:
            file_path (str): The path to the file being tracked.
            size (int): The size of the file in bytes.
            ftime (float): A time of the file (Unix timestamp) to record for syncing.
            bitmask (int): The progress bitmask, default intepretation:
                           - 1 represents incomplete status,
                           - 0 represents complete status,
                           - A bitmask value of 0 indicates that all partitions are completed.
        """  # noqa: D401, D404
        self.lock = asyncio.Lock()

        # file metadata
        self.file_path = file_path
        self.size = size
        self.ftime = ftime

        # progress states
        self.bitmask = bitmask

        # temporay states
        # write_change is for AOF persistence
        # are there changes since load | should we persist this node
        self.write_change = False
        # has this file node caused a failure already
        self.failed = False

    @abstractmethod
    def serialize(self) -> str:
        """Serialize the instance state to a string for persistence. concrete method should choose what to persist."""

    @abstractmethod
    def is_match(self) -> bool:
        """Set condition for the instance matches the system file to ensure it is the same file."""

    @abstractmethod
    def is_sync(self) -> bool:
        """Set condition for the instance matches the system file and it is synced(same file and done)."""

    @classmethod
    def deserialize(cls, state: str):
        """Deserialize a JSON string to a file node.

        This method loads the state of the file node from a JSON string.
        """
        data = json.loads(state)
        ins = cls()
        for key, val in data.items():
            setattr(ins, key, val)
        return ins

    def is_partition_complete(self, partition_id: int) -> bool:
        """Check if a partition is completed."""
        return not bitmask_is_bit_set(self.bitmask, partition_id)

    def get_completed_size(self) -> int:
        """Provide the sum of completed partition sizes in bytes."""
        return self.size - bitmask_set_bit_in_size(self.bitmask, self.size, PARTITION_SIZE)

    async def set_partition_complete(self, partition_id: int):
        """Mark one partition complete."""
        async with self.lock:
            self.bitmask = bitmask_clear_bit(self.bitmask, partition_id)
            self.write_change = True


class UploadFileNode(BaseFileNode):  # noqa: D101
    def __init__(
        self,
        file_path: str = "",
        size: int = -1,
        ftime: float = -1.0,
        bitmask: int = -1,
        upload_id="",
        hash="",
        race_flag=False,
        complete=False,
    ):
        """Initialize the upload file node with additional attributes for upload management.

        This class extends BaseFileNode to include attributes specific to upload management.

        Attributes:
            upload_id (str): Identifier set after initiating a multipart upload.
            hash (str): Hash computed by the worker for the file.
            race_flag (bool): Flag necessary to prevent racing condition when multiple producers
                              send the same workload to the consumer. Only one should succeed.
            complete (bool): Marked complete state unique to multipart upload.
        """
        super().__init__(file_path=file_path, size=size, ftime=ftime, bitmask=bitmask)
        self.upload_id = upload_id
        self.hash = hash
        self.race_flag = race_flag
        self.complete = complete

    def serialize(self):
        """Convert the upload file node state to a string.

        This method converts the upload filenode states to a JSON string representation.
        Unnecessary fields are removed to conserve space in serialization.
        """
        include_fields = ["size", "ftime", "bitmask", "upload_id", "hash", "complete", "file_path"]
        state = {field: getattr(self, field) for field in include_fields}
        return json.dumps(state)

    def is_match(self) -> bool:
        """Check if the instance matches the system file to ensure it is still the same file."""
        # this is the same aws upload sync strategy
        # https://github.com/aws/aws-cli/blob/master/awscli/customizations/s3/syncstrategy/base.py#L226
        return (
            os.path.isfile(self.file_path)
            and self.size == os.path.getsize(self.file_path)
            and self.ftime == os.path.getmtime(self.file_path)
        )

    def is_sync(self) -> bool:
        """Check if the instance still matches the system file and synced with remote."""
        return self.is_match() and self.complete

    async def set_file_hash(self, hash):
        """Set the hash for the file."""
        async with self.lock:
            self.hash = hash
            self.write_change = True

    async def set_complete(self):
        """Mark the file as complete."""
        async with self.lock:
            self.complete = True
            self.write_change = True

    async def set_race_flag_once(self):
        """Determine whether the file should be send to mark completion.

        This method determines whether the file should be send to the consumer
        for further processing. It requires a lock since multiple producers may
        concurrently attempt to send the same workload to the consumer, and the
        consumer take time to perform mark completion.

        Returns:
            bool: True if the file is not yet send to the consumer and additional action is needed,
            False if the file is already or will be send to the consumer no additional action is needed.
        """
        async with self.lock:
            should_mark_complete = (
                (self.bitmask == 0)  # All partitions uploaded
                and self.hash  # Hashing completed
                and (not self.complete)  # Not already marked as complete
                and (not self.race_flag)  # No other worker marking completion
            )
            if should_mark_complete:
                # Block further attempts to mark as complete
                self.race_flag = True
            return should_mark_complete

    async def set_failed_once(self) -> bool:
        """Determine whether the file should be marked as failed.

        This method determines whether the file should be marked as failed and
        further processing. It requires a lock since multiple consumers may concurrently
        attempt to fail the same file, but only one consumer should mark it as failed.

        Returns:
            bool: True if the file is marked as failed and additional action is needed,
            False if the file is already marked as failed and no additional action is needed.
        """
        async with self.lock:
            if self.failed:
                # If already marked as failed, no additional action needed
                return False
            # Mark the file as failed and perform additional action
            self.failed = True
            return True


class DownloadFileNode(BaseFileNode):
    """Placeholder class for extending type hinting and code structure.

    This class serves as a placeholder for extending type hinting and code structure.
    It will be further developed in the future.
    """

    def __init__(self):
        """Initialize the download file node."""
        raise NotImplementedError()

    def serialize(self):
        """Convert the download file node state to a string."""
        raise NotImplementedError()

    def is_match(self) -> bool:
        """Check if the instance matches the system file to ensure it is still the same file."""
        raise NotImplementedError()

    def is_sync(self) -> bool:
        """Check if the instance still matches the system file and synced with remote."""
        raise NotImplementedError()


class BaseCompletionTable(Generic[NodeT], ABC):
    """A base class for managing a completion table for file nodes during file transfer.

    The Completion table manages file nodes using a dictionary (absolute_file_path: file_node),
    tracks their state during file transfer, and provides high-level operations for managing
    file nodes, such as creating, deleting, and checking the status of file nodes.
    """

    def __init__(self, table_file_path=None):
        """Initialize the base completion table.

        Args:
            table_file_path (Optional[str]): The file path to store the table data.

        """
        self.table: Dict[str, NodeT] = {}
        self.table_file_path = table_file_path

    # High level managed file node operations
    @abstractmethod
    def create_file_node(self, file_path: str) -> NodeT:
        """Create a file node for the type of completion table.

        This method should be implemented in child classes to create a specific
        type of file node (e.g., upload or download) based on the transfer type.
        """

    def is_file_match(self, file_path: str) -> bool:
        """Check if the file path is matched with an existing file node."""
        return file_path in self.table and self.table[file_path].is_match()

    def is_file_sync(self, file_path: str) -> bool:
        """Check if the file path is synchronized with an existing file node."""
        return file_path in self.table and self.table[file_path].is_sync()

    def get_file_node(self, file_path: str) -> Union[NodeT, None]:
        """Retrieve the file node for the given file path."""
        return self.table.get(file_path, None)

    def calculate_checked_file_completion(self, file_path: str) -> Tuple[int, int]:
        """Calculate the completion status of a file with integrity check.

        This method calculates the completion status of a file by retrieving the
        file node, checking if it matches the actual file, and then return the
        completed size and completed count.
        """
        fn = self.get_file_node(file_path)
        if fn is None:
            return 0, 0
        if not fn.is_match():
            return 0, 0
        return fn.get_completed_size(), fn.is_sync() * 1

    def get_checked_file_node(self, file_path: str) -> Union[NodeT, None]:
        """Retrieve a checked file node for the given file path with integrity check.

        If the file is synced, it deletes the file node entry from table and return None.
        If the file matches but not synced, it returns the file node.
        If the file does not match or not in table, it creates and returns a new file node.
        """
        if self.is_file_match(file_path):  # filenode matches os file
            if self.is_file_sync(file_path):  # filenode synced, transfer complete
                self.delete_file_node(file_path)  # clear this entry
                return None  # transfer complete, nothing to do
            return self.get_file_node(file_path)  # return this filenode
        return self.create_file_node(file_path)  # get a new file node

    def delete_file_node(self, file_path: str):
        """Delete the file node for the given file path from the table."""
        if file_path in self.table:
            self.table.pop(file_path)

    def save_all_file_nodes(self):
        """Save all file nodes in the table to the `table_file_path` file.

        This method saves the state of all file nodes in the table to file.
        It skips nodes that do not need to write changes.

        This method is typically used during emergency stops to ensure the state
        of the table is preserved.
        """
        if self.table_file_path is None:
            return
        with open(self.table_file_path, "a") as f:
            for _, fn in self.table.items():
                if fn.write_change:
                    f.write(fn.serialize() + "\n")
            # no cleanup, this is probably an emergency stop

    async def async_save_file_node(self, file_path: str):
        """Asynchronously save a specific file node to the `table_file_path` file.

        This method saves the state of a specific file node to file asynchronously.
        It skips nodes that do not have write changes and deletes the file node after a successful write.
        This is typically used in async loop to incrementally write completed file nodes to file,
        so table size is bound.
        """
        if self.table_file_path is None:
            return
        fn = self.get_file_node(file_path)
        if fn is not None and fn.write_change:
            async with aiofiles.open(self.table_file_path, "a") as f:
                await f.write(fn.serialize() + "\n")

            # cleanup on successful write,
            # still in async loop
            self.delete_file_node(file_path)

    def is_table_file_exist(self) -> bool:
        """Check if the `table_file_path` file exists."""
        if self.table_file_path is None:
            return False
        return os.path.isfile(self.table_file_path)

    def remove_table_file(self):
        """Remove the `table_file_path` file from the file system if it exists."""
        if (self.table_file_path is not None) and self.is_table_file_exist():
            os.remove(self.table_file_path)

    def load_table(self, node_class: Type[NodeT]):
        """Load the table from `table_file_path` file.

        This method replays the state of the table from local file,
        deserializing each line to a file node. Later file node entries will overwrite
        earlier ones to ensure the table contains the latest file states.
        """
        if self.table_file_path is None:
            return
        if not self.is_table_file_exist():
            return
        with open(self.table_file_path, "r") as f:
            for line in f.readlines():
                _file_node = node_class.deserialize(line)
                # let later entries overwrite earlier entries
                self.table[_file_node.file_path] = _file_node


class UploadCompletionTable(BaseCompletionTable[UploadFileNode]):
    """A class for managing the upload completion table for file nodes during file upload.

    This class specializes the BaseCompletionTable for managing upload-specific file nodes.
    """

    def create_file_node(self, fp) -> UploadFileNode:
        """Create an upload file node for the given file path.

        This method creates an upload file node based on the file path, size,
        last modified time, and partition count, then adds this entry to the table.
        """
        if not os.path.isfile(fp):
            # normal workflow should never get here
            raise NgcException(f"File path: {fp} which used to create file index is invalid.")

        _file_size = os.path.getsize(fp)
        number_of_file_partitions = (_file_size - 1) // PARTITION_SIZE + 1

        self.table[fp] = UploadFileNode(
            file_path=fp, size=_file_size, ftime=os.path.getmtime(fp), bitmask=2**number_of_file_partitions - 1
        )
        return self.table[fp]

    def load_table(self):
        """Load the table of upload file nodes from the `table_file_path` file."""
        super().load_table(UploadFileNode)


class DownloadCompletionTable(BaseCompletionTable[DownloadFileNode]):
    """A class for managing the download completion table for file nodes during file download.

    This class specializes the BaseCompletionTable for managing download-specific file nodes.
    """

    def create_file_node(self, fp) -> DownloadFileNode:
        """Create a download file node for the given file path."""
        raise NotImplementedError()

    def load_table(self):
        """Load the table of download file nodes from the `table_file_path` file."""
        super().load_table(DownloadFileNode)
