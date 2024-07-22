# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=missing-class-docstring
import traceback
import json
import uuid
from datetime import datetime, timezone
from contextlib import contextmanager
from typing import List
from google.cloud import logging as cloudlogging
from ipulse_shared_core_ftredge.enums.enums_common_utils import TargetLogs, LogLevel, LogStatus
from ipulse_shared_core_ftredge.utils_gcp import write_json_to_gcs


# ["data_import","data_quality", "data_processing","data_general","data_persistance","metadata_quality", "metadata_processing", "metadata_persistance","metadata_general"]

class ContextLog:
    MAX_TRACEBACK_LINES = 14  # Define the maximum number of traceback lines to include
    def __init__(self, level: LogLevel, base_context: str = None, collector_id: str = None,
                 e: Exception = None, e_type: str = None, e_message: str = None, e_traceback: str = None,
                 subject: str = None, description: str = None, context: str = None,
                 log_status: LogStatus = LogStatus.OPEN):
        if e is not None:
            e_type = type(e).__name__ if e_type is None else e_type
            e_message = str(e) if e_message is None else e_message
            e_traceback = traceback.format_exc() if e_traceback is None else e_traceback
        elif e_traceback is None and (e_type or e_message):
            e_traceback = traceback.format_exc()

        self.level = level
        self.subject = subject
        self.description = description
        self._base_context = base_context
        self._context = context
        self.collector_id = collector_id
        self.exception_type = e_type
        self.exception_message = e_message
        self.exception_traceback = self._format_traceback(e_traceback,e_message)
        self.log_status = log_status
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def _format_traceback(self, e_traceback, e_message):
        if not e_traceback or e_traceback == 'None\n':
            return None

        traceback_lines = e_traceback.splitlines()
        
        # Remove lines that are part of the exception message if they are present in traceback
        message_lines = e_message.splitlines() if e_message else []
        if message_lines:
            for message_line in message_lines:
                if message_line in traceback_lines:
                    traceback_lines.remove(message_line)

        # Filter out lines from third-party libraries (like site-packages)
        filtered_lines = [line for line in traceback_lines if "site-packages" not in line]
        
        # If filtering results in too few lines, revert to original traceback
        if len(filtered_lines) < 2:
            filtered_lines = traceback_lines

        # Combine standalone bracket lines with previous or next lines
        combined_lines = []
        for line in filtered_lines:
            if line.strip() in {"(", ")", "{", "}", "[", "]"} and combined_lines:
                combined_lines[-1] += " " + line.strip()
            else:
                combined_lines.append(line)

        # Determine the number of lines to keep from the start and end
        keep_lines_start = min(self.MAX_TRACEBACK_LINES // 2, len(combined_lines))
        keep_lines_end = min(self.MAX_TRACEBACK_LINES // 2, len(combined_lines) - keep_lines_start)

        if len(combined_lines) > self.MAX_TRACEBACK_LINES:
            # Include the first few and last few lines, and an indicator of truncation
            formatted_traceback = '\n'.join(
                combined_lines[:keep_lines_start] + 
                ['... (truncated) ...'] + 
                combined_lines[-keep_lines_end:]
            )
        else:
            formatted_traceback = '\n'.join(combined_lines)

        return formatted_traceback

    @property
    def base_context(self):
        return self._base_context

    @base_context.setter
    def base_context(self, value):
        self._base_context = value

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    def to_dict(self):
        return {
            "base_context": self.base_context,
            "context": self.context,
            "level_code": self.level.value,
            "level_name": self.level.name,
            "subject": self.subject,
            "description": self.description,
            "exception_type": self.exception_type,
            "exception_message": self.exception_message,
            "exception_traceback": self.exception_traceback,
            "log_status": self.log_status.value,
            "collector_id": self.collector_id,
            "timestamp": self.timestamp
        }

class PipelineWatcher:
    ERROR_START_CODE = LogLevel.ERROR.value
    WARNING_START_CODE = LogLevel.WARNING.value
    NOTICE_START_CODE = LogLevel.NOTICE.value
    SUCCESS_START_CODE = LogLevel.SUCCESS.value

    def __init__(self, base_context: str, target_logs: TargetLogs = TargetLogs.MIXED, logger_name=None):
        self._id = str(uuid.uuid4())
        self._logs = []
        self._early_stop = False
        self._errors_count = 0
        self._warnings_count = 0
        self._notices_count = 0
        self._successes_count = 0
        self._level_counts = {level.name: 0 for level in LogLevel}
        self._base_context = base_context
        self._context_stack = []
        self._target_logs = target_logs.value
        self._logger = self._initialize_logger(logger_name)

    def _initialize_logger(self, logger_name):
        if logger_name:
            logging_client = cloudlogging.Client()
            return logging_client.logger(logger_name)
        return None

    @contextmanager
    def context(self, context):
        self.push_context(context)
        try:
            yield
        finally:
            self.pop_context()

    def push_context(self, context):
        self._context_stack.append(context)

    def pop_context(self):
        if self._context_stack:
            self._context_stack.pop()

    @property
    def current_context(self):
        return " >> ".join(self._context_stack)

    @property
    def base_context(self):
        return self._base_context

    @property
    def id(self):
        return self._id

    @property
    def early_stop(self):
        return self._early_stop

    def set_early_stop(self, max_errors_tolerance: int, create_error_log=True, pop_context=False):
        self._early_stop = True
        if create_error_log:
            if pop_context:
                self.pop_context()
            self.add_log(ContextLog(level=LogLevel.ERROR,
                                    subject="EARLY_STOP",
                                    description=f"Total MAX_ERRORS_TOLERANCE of {max_errors_tolerance} has been reached."))

    def reset_early_stop(self):
        self._early_stop = False

    def get_early_stop(self):
        return self._early_stop

    def add_log(self, log: ContextLog):
        if (self._target_logs == TargetLogs.SUCCESSES and log.level >=self.NOTICE_START_CODE) or \
           (self._target_logs == TargetLogs.WARNINGS_AND_ERRORS and log.level.value < self.WARNING_START_CODE):
            raise ValueError(f"Invalid log level {log.level.name} for Pipeline Watcher target logs setup: {self._target_logs}")
        log.base_context = self.base_context
        log.context = self.current_context
        log.collector_id = self.id
        log_dict = log.to_dict()
        self._logs.append(log_dict)
        self._update_counts(log_dict)

        if self._logger:
            # We specifically want to avoid having an ERROR log level for this structured Pipeline Watcher reporting, to ensure Errors are alerting on Critical Application Services.
            # A single ERROR log level can be used for the entire pipeline, which shall be used at the end of the pipeline
            if log.level.value >= self.WARNING_START_CODE:
                self._logger.log_struct(log_dict, severity="WARNING")
            elif log.level.value >= self.NOTICE_START_CODE:
                self._logger.log_struct(log_dict, severity="NOTICE")
            else:
                self._logger.log_struct(log_dict, severity="INFO")

    def add_logs(self, logs: List[ContextLog]):
        for log in logs:
            self.add_log(log)

    def clear_logs_and_counts(self):
        self._logs = []
        self._errors_count = 0
        self._warnings_count = 0
        self._notices_count = 0
        self._successes_count = 0
        self._level_counts = {level.name: 0 for level in LogLevel}

    def clear_logs(self):
        self._logs = []

    def get_all_logs(self):
        return self._logs

    def get_logs_for_level(self, level: LogLevel):
        return [log for log in self._logs if log["level_code"] == level.value]

    def get_logs_by_str_in_context(self, context_substring: str):
        return [
            log for log in self._logs
            if context_substring in log["context"]
        ]

    def contains_errors(self):
        return self._errors_count > 0

    def count_errors(self):
        return self._errors_count

    def contains_warnings_or_errors(self):
        return self._warnings_count > 0 or self._errors_count > 0

    def count_warnings_and_errors(self):
        return self._warnings_count + self._errors_count

    def count_warnings(self):
        return self._warnings_count

    def count_notices(self):
        return self._notices_count

    def count_successes(self):
        return self._successes_count

    def count_all_logs(self):
        return len(self._logs)

    def count_logs_by_level(self, level: LogLevel):
        return self._level_counts.get(level.name, 0)

    def _count_logs(self, context_substring: str, exact_match=False, level_code_min=None, level_code_max=None):
        return sum(
            1 for log in self._logs
            if (log["context"] == context_substring if exact_match else context_substring in log["context"]) and
               (level_code_min is None or log["level_code"] >= level_code_min) and
               (level_code_max is None or log["level_code"] <= level_code_max)
        )

    def count_logs_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True)

    def count_logs_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context)

    def count_logs_by_level_for_current_context(self, level: LogLevel):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=level.value, level_code_max=level.value)

    def count_logs_by_level_for_current_and_nested_contexts(self, level: LogLevel):
        return self._count_logs(self.current_context, level_code_min=level.value, level_code_max=level.value)

    def count_errors_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=self.ERROR_START_CODE)

    def count_errors_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context, level_code_min=self.ERROR_START_CODE)

    def count_warnings_and_errors_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=self.WARNING_START_CODE)

    def count_warnings_and_errors_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context, level_code_min=self.WARNING_START_CODE)

    def count_warnings_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=self.WARNING_START_CODE, level_code_max=self.ERROR_START_CODE - 1)

    def count_warnings_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context, level_code_min=self.WARNING_START_CODE, level_code_max=self.ERROR_START_CODE - 1)

    def count_notices_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=self.NOTICE_START_CODE, level_code_max=self.WARNING_START_CODE-1)

    def count_notices_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context, level_code_min=self.NOTICE_START_CODE, level_code_max=self.WARNING_START_CODE-1)

    def count_successes_for_current_context(self):
        return self._count_logs(self.current_context, exact_match=True, level_code_min=self.SUCCESS_START_CODE, level_code_max=self.NOTICE_START_CODE-1)

    def count_successes_for_current_and_nested_contexts(self):
        return self._count_logs(self.current_context, level_code_min=self.SUCCESS_START_CODE, level_code_max=self.NOTICE_START_CODE-1)

    def export_logs_to_gcs_file(self, bucket_name, storage_client, file_prefix=None, file_name=None, top_level_context=None, save_locally=False, local_path=None, logger=None, max_retries=2):
        def log_message(message):
            if logger:
                logger.info(message)

        def log_error(message, exc_info=False):
            if logger:
                logger.error(message, exc_info=exc_info)

        if not file_prefix:
            file_prefix = self._target_logs
        if not file_name:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            if top_level_context:
                file_name = f"{file_prefix}_{timestamp}_{top_level_context}_len{len(self._logs)}.json"
            else:
                file_name = f"{file_prefix}_{timestamp}_len{len(self._logs)}.json"

        result = None
        try:
            result = write_json_to_gcs(
                bucket_name=bucket_name,
                storage_client=storage_client,
                data=self._logs,
                file_name=file_name,
                save_locally=save_locally,
                local_path=local_path,
                logger=logger,
                max_retries=max_retries,
                overwrite_if_exists=False
            )
            log_message(f"{file_prefix} successfully saved (overwritten={result.get('gcs_file_overwritten')}) to GCS at {result.get('gcs_path')} and locally at {result.get('local_path')}.")
        except Exception as e:
            log_error(f"Failed at export_logs_to_gcs_file for {file_prefix} for file {file_name} to bucket {bucket_name}: {type(e).__name__} - {str(e)}")

        return result

    def import_logs_from_json(self, json_or_file, logger=None):
        def log_message(message):
            if logger:
                logger.info(message)

        def log_warning(message, exc_info=False):
            if logger:
                logger.warning(message, exc_info=exc_info)

        try:
            if isinstance(json_or_file, str):  # Load from string
                imported_logs = json.loads(json_or_file)
            elif hasattr(json_or_file, 'read'):  # Load from file-like object
                imported_logs = json.load(json_or_file)
            self.add_logs(imported_logs)
            log_message("Successfully imported logs from json.")
        except Exception as e:
            log_warning(f"Failed to import logs from json: {type(e).__name__} - {str(e)}", exc_info=True)

    def _update_counts(self, log, remove=False):
        level_code = log["level_code"]
        level_name = log["level_name"]

        if remove:
            if level_code >= self.ERROR_START_CODE:
                self._errors_count -= 1
            elif self.WARNING_START_CODE <= level_code < self.ERROR_START_CODE:
                self._warnings_count -= 1
            elif self.NOTICE_START_CODE <= level_code < self.WARNING_START_CODE:
                self._notices_count -= 1
            elif self.SUCCESS_START_CODE <= level_code < self.NOTICE_START_CODE:
                self._successes_count -= 1
            self._level_counts[level_name] -= 1
        else:
            if level_code >= self.ERROR_START_CODE:
                self._errors_count += 1
            elif self.WARNING_START_CODE <= level_code < self.ERROR_START_CODE:
                self._warnings_count += 1
            elif self.NOTICE_START_CODE <= level_code < self.WARNING_START_CODE:
                self._notices_count += 1
            elif self.SUCCESS_START_CODE <= level_code < self.NOTICE_START_CODE:
                self._successes_count += 1
            self._level_counts[level_name] += 1